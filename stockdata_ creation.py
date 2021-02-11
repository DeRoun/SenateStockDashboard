# script to both download stock data and turn it into a dataframe to be saved
# as a .csv file
import yfinance as yf
import pandas as pd
from data_prep import s_trans

# loop each stock ticker into new dataframe gathering info on 3 month before 
# and after purchase
stock_data = pd.DataFrame()
for i in s_trans.index:
        # download stock data for each senator transaction
        start = s_trans['period_start'].values[i]
        end = s_trans['period_end'].values[i]
        tick_id = s_trans['ticker'].values[i]
        stock = []
        stock = yf.download(tick_id, start = start, end = end, progress=False)
        stock['Name'] = tick_id
        stock_data = stock_data.append(stock, sort=False)

# set row names to first column
stock_data.index.name = 'date'
stock_data.reset_index(inplace=True)
stock_data = stock_data.drop(['Volume', 'Open', 'High', 'Low', 'Close'],
                             axis=1).drop_duplicates()
stock_data.columns = ['date', 'close', 'ticker']
stock_data['date'] = pd.to_datetime(stock_data['date']).dt.date

# download downloaded data as csv to reduce other script's run time
stock_data.to_csv('data/stock_data.csv', index=False, header=True)