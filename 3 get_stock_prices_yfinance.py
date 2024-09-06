# -*- coding: utf-8 -*-
"""
Created on Sat Aug 31 07:45:41 2024

@author: Lukasz Macias
"""

# -----------------------------------------------------------------------------

import yfinance as yf
import pandas as pd

def get_stock_price(ticker):
    ticker = ticker 
    period = '5y'
    prices = yf.download(ticker, period=period, interval='1d')
    
    prices['daily_volatility'] = prices['High'] - prices['Low'] 
    prices['daily_movement'] = prices['Close'] - prices['Open'] 
    
    return prices

# Fetch the Tesla stock price history for the last year
df = get_stock_price('TSLA')

df.to_excel('tsla_prices_5y.xlsx')

# -----------------------------------------------------------------------------