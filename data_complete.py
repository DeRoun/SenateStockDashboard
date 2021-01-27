import pandas as pd
import numpy as np
import datetime
from data_prep import s_trans

# create stock data df
stock_data = pd.read_csv ('data/stock_data.csv')

# rename stock data columns and conver date column to date d.type
stock_data.columns = ['date', 'close', 'ticker']
stock_data['date'] = pd.to_datetime(stock_data['date']).dt.date

# merge s_trans and stock_data to have the stock price the senator paid that day (closing price) as final
s_trans.rename(columns = {'transaction_date' : 'date'}, inplace = True)
final = s_trans.merge(stock_data, on=['date', 'ticker'], how = 'left').drop_duplicates(subset='trade_id')

# create new max/min column
final['max/min'] = np.nan

# create list of trade_ids
trade = final['trade_id'].tolist()
print(trade[0])

# create for loop that writes to the max/min column
count = 0
for i in trade:
        #make temp dataframe
        temp = []

        # gets the start and end date form s_trans table for the current index of the trade list
        start = pd.to_datetime(final.loc[final['trade_id'] == trade[count], 'period_start'].iloc[0]).date()
        end = pd.to_datetime(final.loc[final['trade_id'] == trade[count], 'period_end'].iloc[0]).date()

        # gets the name of the ticker for the current index of the trade list
        tick_id = final.loc[final['trade_id'] == trade[count], 'ticker'].iloc[0]

        # gets the type (Sale or Purchase) of the current index of the trade list
        type = final.loc[final['trade_id'] == trade[count], 'type']

        # make subset dataframe of ticker within date range
        temp = stock_data[(stock_data.ticker == tick_id) & (stock_data["date"].isin(pd.date_range(start, end)))]

        # will write either the min or max of the current index of the trade list to the max/min column
        # of the s_trans data frame
        if 'Sale' in type:
            final.loc[final['trade_id'] == trade[count], 'max/min'] = temp['close'].argmax()
            count += 1
        else:
            final.loc[final['trade_id'] == trade[count], 'max/min'] = temp['close'].argmin()
            count += 1

# create a new column called accuracy, calculates the percent difference between max/min and price

final['accuracy'] = (final['max/min'] / final['price']) * 100