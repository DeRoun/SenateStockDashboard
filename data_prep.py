import pandas as pd
import numpy as np
import datetime

# initial read/creation of senator transaction csv
s_trans = pd.read_csv ('data/senator_transactions.csv')

# clean csv to showcase only trackable stock trades i.e in stock market database (ONLY PURCHASE AND SALE TYPE)
keep_type = np.array(['Corporate Bond', 'Other Securities', 'Stock'])
s_trans = s_trans[s_trans.asset_type.isin(keep_type)]
s_trans = s_trans[s_trans.type != 'Exchange']
s_trans = s_trans[s_trans.ticker != '--']
s_trans = s_trans.drop(columns=['comment', 'ptr_link'])
s_trans['trade_id'] = s_trans.index + 1

# add column that is 3 months before and after transaction date, both MIN AND MAX

# format transaction date data into date format
s_trans['transaction_date']= pd.to_datetime(s_trans['transaction_date']).dt.date

# add three month interval to create interval columns
three_month = datetime.timedelta(3*365/12)

# set interval column dates to be 3 months before and after purchase date, except when three months past
# is a future date (then set as current date)
s_trans['period_end'] = np.where(s_trans['transaction_date'] + three_month >= datetime.date.today(),
                                 datetime.date.today(),
                                 s_trans['transaction_date'] + three_month)

s_trans['period_start'] = s_trans['transaction_date'] - three_month

# create stock data df
stock_data = pd.read_csv ('data/stock_data.csv')

# rename stock data columns and conver date column to date d.type
stock_data.columns = ['date', 'close', 'ticker']
stock_data['date'] = pd.to_datetime(stock_data['date']).dt.date

# merge s_trans and stock_data to have the stock price the senator paid that day (closing price) as final
s_trans.rename(columns = {'transaction_date' : 'date'}, inplace = True)
final = s_trans.merge(stock_data, on=['date', 'ticker'], how = 'left').drop_duplicates(subset='trade_id')

#create new max/min column
final['max/min'] = np.nan

# create list of trade_ids
trade = final['trade_id'].tolist()

# create for loop that writes to the max/min column
count = 0
for i in trade:
        #make temp dataframe
        temp = []

        # gets the start and end date form s_trans table for the current index of the trade list
        start = pd.to_datetime(final.loc[final['trade_id'] == trade[count], 'period_start'].iloc[0]).date()
        end = pd.to_datetime(final.loc[final['trade_id'] == trade[count], 'period_end'].iloc[0]).date()

        # gets the name of the ticker for the current index of the trade list
        tick_id = final.loc[final['trade_id'] == trade[count], 'ticker']

        # gets the type (Sale or Purchase) of the current index of the trade list
        type = final.loc[final['trade_id'] == trade[count], 'type']

        # make subset dataframe of ticker within date range #### GETTING ERROR HERE####
        temp = stock_data[stock_data['ticker'] == tick_id & (stock_data['date'] > start) & (stock_data['date'] <= end)]

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