# Senate Stock Dashboard
A data visualization on both the accuracy and amount of stock trades reported by by senators under the STOCK act since 2012.

**Code and Data behind for [Senate Stock Dashboard](deroun.com) project:**

- `Data/senate_transactions.csv`: raw data of states gun deaths collected from [Senate Stock Watch](https://senatestockwatcher.com/api.html)
- `Data/stock_data.csv`: raw data created using Yahoo! finance data thats to the [Python yfinace package](https://pypi.org/project/yfinance/)
- `data_complete.py`: TBD
- `data_prep.py`: creates stock transaction data frame, along with basic cleaning to be used for both the final dataframe and in the creation of stock_data
- `stockdata_creation.py`: code that uses the yfinance package to download the needed stock data within a 6 month period of each trade, then saves it as a csv for ease of use