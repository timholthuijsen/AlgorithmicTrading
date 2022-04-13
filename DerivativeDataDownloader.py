# from yfinance_multiple_tickers import *
import copy
import datetime as dt
import yfinance as yf
import pandas as pd 

tickers = ["AMZN","MSFT","GOOG","ECH","BLDP"]

# Create a percentage return dataframe called return_df
def returns(interval, tickers = tickers[:20], delta = 3650):
    print('interval is: ', interval)
    print('delta is:',delta)
    ohlc_mon = {} # directory with ohlc value for each stock            
    start = dt.datetime.today()-dt.timedelta(delta)
    end = dt.datetime.today()
    
    # looping over tickers and creating a dataframe with close prices
    for ticker in tickers:
        print("interval is still: ", interval)
        ohlc_mon[ticker] = yf.download(ticker,start,end,interval='1d')
        ohlc_mon[ticker].dropna(inplace=True,how="all")
     
    tickers = ohlc_mon.keys() # redefine tickers variable after removing any tickers with corrupted data
    
    ################################Backtesting####################################
    
    # calculating monthly return for each stock and consolidating return info by stock in a separate dataframe
    ohlc_dict = copy.deepcopy(ohlc_mon)
    # Create a percentage return dataframe called return_df
    return_df = pd.DataFrame()
    for ticker in tickers:
        print("calculating monthly return for ",ticker)
        ohlc_dict[ticker]["mon_ret"] = ohlc_dict[ticker]["Adj Close"].pct_change()
        return_df[ticker] = ohlc_dict[ticker]["mon_ret"]
    #return_df.dropna(inplace=True)
    return return_df

#returndata = returns(tickers = tickers[:35], interval = '1d', delta = 365)


#made specifically to write returns pct change to csv
def csvwriter(number = len(tickers)):
    data = returns(interval = '1d', tickers = ["AMZN","MSFT","GOOG","ECH","BLDP"], delta = 730)
    print(data.shape)
    data.to_csv('data/DailyIntervalDerivative.csv')
    return data.shape

csvwriter()
    
    