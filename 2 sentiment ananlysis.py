# -*- coding: utf-8 -*-
"""
Created on Tue Sep  3 15:40:06 2024

@author: Lukasz Macias
"""
import pandas as pd 
from textblob import TextBlob
import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
nltk.download('vader_lexicon')

tsla = pd.read_excel('TSLA_comments.xlsx')

# tsla = tsla.head(1000)

# ---------------------------------------------------------------------------------

# demo 
text = "great stock to buy!"
blob = TextBlob(text)
sentiment = blob.sentiment 
print(sentiment)

# demo vader 
 
# initalize VADER analyzer 
sia = SentimentIntensityAnalyzer()

# demo 
sentiment = sia.polarity_scores("This is a great day!")
print(sentiment) 

sentiment = sia.polarity_scores("This is a terrible day!")
print(sentiment) 

sentiment = sia.polarity_scores("<p>Elon lost UK, Europe and now Brazil. </p>")
print(sentiment) 

# ---------------------------------------------------------------------------------
# -- APPLY TEXT BLOB --

def get_sentiment(text):
    try:
        blob = TextBlob(text)
        return blob.sentiment.polarity, blob.sentiment.subjectivity
    except Exception as e2:
        print(f"An unexpected error occurred: {e2}")
        return None

# Apply the function and unpack the result into two new columns
tsla[['sentiment_polarity', 'sentiment_subjectivity']] = tsla['text'].apply(get_sentiment).apply(pd.Series)

"""
Polarity: The score shows whether the sentence is positive or negative. 
In this case, "love" is positive, so the score will be closer to 1.

Subjectivity: If the sentence expresses an opinion, the subjectivity score will be high (closer to 1).
 If it's more of a fact, it will be closer to 0.
"""
# ---------------------------------------------------------------------------------

def senti_polarity_tag(x):
    if x < 0:
        return 'NEGATIVE'
    elif x == 0:
        return 'NEUTRAL'
    elif x > 0:
        return 'POSITIVE'
    else:
        return 'N/A'
    
tsla['senti_polarity_tag'] = tsla['sentiment_polarity'].apply(senti_polarity_tag)

# ---------------------------------------------------------------------------------
# -- APPLY VADER --

def get_sentiment_score(x): 
    try:
        return sia.polarity_scores(x)
    except AttributeError:
        return None

tsla['vader_senti_score_full'] = tsla['text'].apply(get_sentiment_score)

vader_decomposed = pd.json_normalize(tsla['vader_senti_score_full']).add_prefix('vader_')

tsla = pd.concat([tsla, vader_decomposed], axis=1)

# -------------------------------------------------------------------------------
# create a master sentiment attribute
# 1) Sentiment Tag from YFinanace (bullish = 1, bearish =- neutral = 0)
# 2) if None --> take the sentiment score from TextBlob/Vader as a best estimate 

def check_sentiment_tb(row):
    if pd.isna(row['sent_tag_score']):  
        return row['sentiment_polarity']  
    else:
        return row['sent_tag_score']  

def check_sentiment_vader(row):
    if pd.isna(row['sent_tag_score']):  
        return row['vader_compound'] 
    else:
        return row['sent_tag_score']  

tsla['final_sentiment_textblob'] = tsla.apply(check_sentiment_tb, axis=1)
tsla['final_sentiment_vader'] = tsla.apply(check_sentiment_vader, axis=1)

tsla_head =tsla.head(1000)

tsla.to_excel('TSLA_sentiment.xlsx')













