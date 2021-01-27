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
s_trans['trade_id'] = s_trans.reset_index().index + 1

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