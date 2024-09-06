# -*- coding: utf-8 -*-
"""
Created on Sat Aug 31 11:49:23 2024

@author: PC
"""

import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns


df = pd.read_excel('TSLA_sentiment.xlsx')

'''
Article on sentiment analysis: 

https://medium.com/@rslavanyageetha/vader-a-comprehensive-guide-to-sentiment-analysis-in-python-c4f1868b0d2e
'''

# ---------------------------------------------------------------------------------------
# which model to choose: Vader or Text Blob ? 

df[['vader_compound', 'sentiment_polarity']].describe()

# create a histogram comapring TextBlob to Vader 

plt.figure(figsize=(10, 6))

plt.hist(df['vader_compound'], bins=20, alpha=0.5, label='VADER Compound', color='blue', edgecolor='black')
plt.hist(df['sentiment_polarity'], bins=20, alpha=0.5, label='TextBlob Polarity', color='orange', edgecolor='black')

plt.title('Comparison of VADER Compound and TextBlob Sentiment Polarity', fontsize=16)
plt.xlabel('Sentiment Score', fontsize=14)
plt.ylabel('Frequency', fontsize=14)
plt.legend(loc='upper right')
plt.show()

# create a box plot 

plt.figure(figsize=(8, 6))

sns.boxplot(data=df[['vader_compound', 'sentiment_polarity']])

plt.title('Box Plot of VADER Compound and TextBlob Sentiment Polarity', fontsize=16)
plt.xlabel('Sentiment Metrics', fontsize=14)
plt.ylabel('Sentiment Score', fontsize=14)

plt.show()

# Which of the models makes more sense looking at the actual text interpretations

# violin plot for compound sentiment score Label + Vader or TextBlob

plt.figure(figsize=(8, 6))
sns.violinplot(data=df[['final_sentiment_textblob', 'final_sentiment_vader']])

plt.title('Violin Plot of Final Sentiment (TextBlob vs VADER)', fontsize=16)
plt.xlabel('Sentiment Metrics', fontsize=14)
plt.ylabel('Sentiment Score', fontsize=14)

plt.show()

# -------------------------------------------------------------------------------------

df['time'] = pd.to_datetime(df['time'])
df_daily_counts = df.groupby(df['time'].dt.date).size()

plt.figure(figsize=(10, 6))
df_daily_counts.plot(kind='line', color='blue')

plt.title('Number of comments by Day', fontsize=16)
plt.xlabel('Date', fontsize=14)
plt.ylabel('Number of comments per day', fontsize=14)

plt.grid(True)
plt.show()

# -----------------------------------------------------------------------------------

df['time'] = pd.to_datetime(df['time'])
df['date'] = df['time'].dt.date
daily_counts = df.groupby('date').size().reset_index(name='comment_count')

plt.figure(figsize=(10, 6))
sns.boxplot(y=daily_counts['comment_count'])

plt.title('Box Plot of Number of Comments per Day', fontsize=16)
plt.ylabel('Number of Comments', fontsize=14)

plt.show()

daily_counts.describe()









