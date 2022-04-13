import datetime as dt
import yfinance as yf
import pandas as pd



def generate_all_tickers(csv = 'data/Tickers.csv'):
    #Getting all ticker names from the csv
    csv = pd.read_csv(csv)
    tickercsv = csv['Name']
    tickers = [] 
    for ticker in tickercsv:
        tickers.append(ticker)
    return tickers


def download(tickers= ["AMZN","MSFT","GOOG","ECH","BLDP"], interv = '1d',
             start = dt.datetime.today()-dt.timedelta(730), end = dt.datetime.today()):
    cl_price=pd.DataFrame()
    for ticker in tickers:
        cl_price = yf.download(ticker,start,end, interval=interv)#["Adj Close"]
    # cl_price.dropna(axis=0,how='any',inplace=True)
    
    return cl_price
    
def csv_writer(data, filename):
    data.to_csv(filename, date_format = '%Y-%m-%d')
    
    
#download ticker data:
# csv_writer(download(tickers = "GOOG",start = dt.datetime.today()-dt.timedelta(730),interv = '1d'), 'data/GoogleOHLCV.csv')

#Write a csv datafile for limited tickers:
# csv_writer(download(interv='1d', start= dt.datetime.today()-dt.timedelta(730)),'data/stockdata.csv')