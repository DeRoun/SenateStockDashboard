import pandas as pd
import numpy as np
import yfinance as yf
import datetime

# initial read/creation of senator transaction csv
s_trans = pd.read_csv ('data/senator_transactions.csv')

# clean csv to showcase only trackable stock trades i.e in stock market database (ONLY PURCHASE AND SALE TYPE)
keep_type = np.array(['Corporate Bond', 'Other Securities', 'Stock'])
s_trans = s_trans[s_trans.asset_type.isin(keep_type)]
s_trans = s_trans[s_trans.type != 'Exchange']
s_trans = s_trans[s_trans.ticker != '--']
s_trans = s_trans.drop(columns=['comment', 'ptr_link'])

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

########################################################################################################################

# create df for stock information
stock_data = pd.DataFrame()

# make a lilst of all tickers from s_trans df
tick = s_trans['ticker'].head(10).tolist()

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

#clean stock data before save
stock_data = stock_data.drop(['Volume', 'Open', 'High', 'Low', 'Close'], axis=1)
stock_data['Date']= pd.to_datetime(stock_data['Date']).dt.date

# download downloaded data as csv to reduce script run time
stock_data.to_csv('data\stock_data.csv', index=False, header=True)