# script to format data to easily be used in a dashboard, saving the final
# data as a .csv file
import pandas as pd
import numpy as np
from data_prep import s_trans

# create stock data df and unavailable df
stock_data = pd.read_csv('data/stock_data.csv')
unavailable = pd.read_csv('data/unavailable.csv')

# removes transactions from df where the data was unavailble through yfinance
unavailable = unavailable['Ticker'].tolist()
s_trans = s_trans[~s_trans.ticker.isin(unavailable)]

# merge s_trans and stock_data to have the stock price the senator paid that
# day (closing price) for final df
s_trans.rename(columns={'transaction_date': 'date'}, inplace=True)
stock_data['date'] = pd.to_datetime(stock_data['date']).dt.date
final = s_trans.merge(stock_data, on=['date', 'ticker'], how='left')

# create new max/min column and resets index of final df
final['max/min'] = np.nan
final.reset_index(drop=True, inplace=True)

# create for loop that writes to the max/min column for each trade
for i in final.index:
        # gets the start, end, tick_id, and transation type from final df 
        # for the current index of the loop
        start = final['period_start'].values[i]
        end = final['period_end'].values[i]
        tick_id = final['ticker'].values[i]
        t_type = final['type'].values[i]

        # will write either the min or max of the current index of the trade
        # list to the max/min column of the final data frame 
        final['max/min'].values[i] = np.where('Sale' in t_type,
                                        stock_data[(stock_data['ticker']
                                                    == tick_id) &
                                                   (stock_data['date'].between(
                                                       start, end))].close.max(),
                                        stock_data[(stock_data['ticker']
                                                    == tick_id) &
                                                   (stock_data['date'].between(
                                                       start, end))].close.min())

# create a new column called accuracy, calculates the percent difference 
# between max/min and close fro date of purchase or sale
final['perc_off'] = abs((100* final['close'] / final['max/min'])-100)

# writes final df to csv for shorter script time for dashboard
final.to_csv('data/final.csv', index=False, header=True)