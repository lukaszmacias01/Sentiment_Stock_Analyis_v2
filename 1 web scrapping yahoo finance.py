# -*- coding: utf-8 -*-
"""
Created on Tue Sep  3 04:36:39 2024

@author: Lukasz Macias
"""

import requests 
import json 
from bs4 import BeautifulSoup
import pandas as pd 
import numpy as np
import re

url = 'https://finance.yahoo.com/quote/AAPL/community/'

response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/110.0'})

soup = BeautifulSoup(response.text)

def extract_tag(text):
    
    bearish = "BEARISH"
    bullish = "BULLISH"
    neutral = "NEUTRAL"
    
    try: 
    
        if re.search(rf'\b{bearish}\b', text):
            return ('BEARISH', -1)
        if re.search(rf'\b{bullish}\b', text):
            return ('BULLISH', 1)  
        if re.search(rf'\b{neutral}\b', text):
            return ('NEUTRAL', 0) 
        else:
            return (None, None)
        
    except TypeError as e:
        print(f'type error {e}')
        return (None, None)

def get_comments(count, offset):
    
    try:

        data = json.loads(soup.select_one('#spotim-config').get_text(strip=True))['config']
        
        url = "https://api-2-0.spot.im/v1.0.0/conversation/read"
        payload = json.dumps({
          "conversation_id": data['spotId'] + data['uuid'].replace('_', '$'),
          "count": count,
          "offset": offset
        })
        headers = {
          'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/110.0',
          'Content-Type': 'application/json',
          'x-spot-id': data['spotId'],
          'x-post-id': data['uuid'].replace('_', '$'),
        }
        
        response = requests.post(url, headers=headers, data=payload)
        data = response.json()
          
        comments = data['conversation']['comments']
          
        df = pd.DataFrame(comments)
        
        # df = df[['time', 'content']]
        
        df = df[['time', 'content', 'additional_data']]
        
        df['content'] = df['content'].apply(lambda x: x[0])
        
        content_expanded = df['content'].apply(pd.Series)
        
        df = pd .concat([df.drop(columns=['content']), content_expanded], axis=1)
        
        df['time'] = pd.to_datetime(df['time'], unit='s')
        
        df['sentiment_tag_tuple'] = df['additional_data'].astype(str)
        df['sentiment_tag_tuple'] = df['sentiment_tag_tuple'].apply(extract_tag)
     
        
        df[['senti_tag', 'sent_tag_score']] = pd.DataFrame(df['sentiment_tag_tuple'].tolist(), index=df.index)

        return df[['time', 'text', 'additional_data', 'sentiment_tag_tuple', 'senti_tag','sent_tag_score']]

    except KeyError as e1:
        print(f"Key error occurred: {e1}")
        return None 
    except Exception as e2:
        print(f"An unexpected error occurred: {e2}")
        return None

# ---------------------------------------------------------------------------------------

offsets = []       
 
for i in range(1, 500000, 50):
    offsets.append(i)  
    
df = get_comments(1, 1) # initialize a DF 

for i in offsets:
    df_append = get_comments(50, i)
    df = pd.concat([df, df_append], ignore_index=True)
    print(i)
    
print('I am done!')

df.to_excel('aapl_comments.xlsx')

   




