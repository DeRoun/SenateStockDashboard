# script to both download stock data and create a into a dataframe to be saved as a .csv file

import pandas as pd
import numpy as np
import yfinance as yf
import datetime
from data_prep import s_trans

# create df for stock information
stock_data = pd.DataFrame()

# make a list of all tickers from s_trans df
tick = s_trans['ticker'].tolist()

# loop each stock ticker into new dataframe gathering info on 3 month before and after purchase
count = 0
for i in tick:
        # download stock data
        stock = []
        start = pd.to_datetime(s_trans.loc[s_trans['ticker'] == tick[count], 'period_start'].iloc[0]).date()
        end = pd.to_datetime(s_trans.loc[s_trans['ticker'] == tick[count], 'period_end'].iloc[0]).date()
        stock = yf.download(i, start = start, end = end, progress=False)
        count += 1

        # add each stock and data to the new dataframe
        if len(stock) == 0:
            None
        else:
            stock['Name'] = i
            stock_data = stock_data.append(stock, sort=False)

# set row names to first column
stock_data.index.name = 'Date'
stock_data.reset_index(inplace=True)

# clean stock data before save
stock_data = stock_data.drop(['Volume', 'Open', 'High', 'Low', 'Close'], axis=1)
stock_data['Date']= pd.to_datetime(stock_data['Date']).dt.date

# download downloaded data as csv to reduce script run time
stock_data.to_csv('data\stock_data.csv', index=False, header=True)