# -*- coding: utf-8 -*-
"""
Created on Fri Sep  6 08:29:12 2024

@author: PC
"""

import pandas as pd 
import matplotlib.pyplot as plt 

# -------------------------------------------------------------------------

f = pd.read_excel('TSLA_sentiment_part_1.xlsx')
f2 = pd.read_excel('TSLA_sentiment_part_2.xlsx')
f3 = pd.read_excel('TSLA_sentiment_part_3.xlsx')

TSLA_sentiment = pd.concat([f, f2, f3], ignore_index=True)

TSLA_prices = pd.read_excel('tsla_prices_5y.xlsx')

# --------------------------------------------------------------------------

TSLA_sentiment['Date'] = pd.to_datetime(TSLA_sentiment['time']).dt.strftime('%Y-%m-%d')

TSLA_senti_agg_day = TSLA_sentiment.groupby('Date').agg({
    'final_sentiment_textblob': ['mean','std'],
    'final_sentiment_vader': ['mean','std', 'count'],
    'sent_tag_score': ['mean','std'] 
}).reset_index()

TSLA_senti_agg_day.columns = ['Date','textblob_mean','textblob_std',
                              'vader_mean','vader_std',
                              'comments_count',
                              'tag_mean', 'tag_std']

# ----------------------------------------------------------------------------

TSLA_senti_agg_day['Date'] = pd.to_datetime(TSLA_senti_agg_day['Date'])

TSLA_merged = pd.merge(TSLA_senti_agg_day, TSLA_prices, on='Date', how='inner')

start = '2023-01-01'
end = '2024-08-30'

TSLA_merged = TSLA_merged[(TSLA_merged['Date'] >= start) & (TSLA_merged['Date'] <= end)]

# ---------------------------------------------------------------------------
# add running AVG. 

TSLA_merged.set_index('Date', inplace = True)

window = 5 

TSLA_merged['textblob_mean_running_avg'] = TSLA_merged['textblob_mean'].rolling(window=window).mean()
TSLA_merged['vader_running_avg'] = TSLA_merged['vader_mean'].rolling(window=window).mean()
TSLA_merged['Close_running_avg'] = TSLA_merged['Close'].rolling(window=window).mean()

TSLA_merged.reset_index(inplace=True)

# -----------------------------------------------------------------------------
# plot sentiment and close price 

TSLA_merged.set_index('Date', inplace = True)

fig, ax1 = plt.subplots(figsize=(14, 7))

label = 'Sentiment score running avg (5 days)'
ax1.set_title('Running Averages of Sentiment Scores and TSLA Closing Prices (5 days)')
ax1.plot(TSLA_merged.index, TSLA_merged['vader_running_avg'], label=label, color='orange')
ax1.set_ylabel('Sentiment Score')
ax1.legend(loc='upper left')
ax1.tick_params(axis='y')

label2 = 'TSLA Closing price running avg (5 days)'
ax2 = ax1.twinx()
ax2.plot(TSLA_merged.index, TSLA_merged['Close_running_avg'], label=label2, color='red', linestyle='--')
ax2.set_ylabel('Closing Price')
ax2.legend(loc='upper right')
ax2.tick_params(axis='y')

plt.xticks(rotation=45)
plt.tight_layout()

TSLA_merged.reset_index(inplace=True)

plt.show()

# ------------------------------------------------------------------------------

TSLA_merged.to_excel('FINAL sentiment and price per day.xlsx')

































