

import datetime as dt
import yfinance as yf
import pandas as pd
import pandas as pd

#Getting all ticker names from the csv
csv = pd.read_csv(r'Tickers.csv')
tickercsv = csv['Name']
tickers = []

for ticker in tickercsv:
    tickers.append(ticker)
    

stocks = ["AMZN","MSFT","INTC","GOOG","INFY.NS","3988.HK","BLDP"]
start = dt.datetime.today()-dt.timedelta(730)
end = dt.datetime.today()
cl_price = pd.DataFrame() # empty dataframe which will be filled with closing prices of each stock
ohlcv_data = {} # empty dictionary which will be filled with ohlcv dataframe for each ticker

# looping over tickers and creating a dataframe with close prices
# fast runtime with: for ticker in stocks
def download(tickers, number):
    for ticker in tickers:
        cl_price[ticker] = yf.download(ticker,start,end)["Adj Close"]
    

# looping over tickers and storing OHLCV dataframe in dictionary
#for ticker in stocks:
#    ohlcv_data[ticker] = yf.download(ticker,start,end)
    
#download(tickers, 20)
    
cl_price.dropna(axis=0,how='any',inplace=True)


