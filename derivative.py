from yfinance_multiple_tickers import *
import copy


# Create a percentage return dataframe called return_df
def returns(tickers = tickers[:20], interval = '1mo', delta = 3650):
    ohlc_mon = {} # directory with ohlc value for each stock            
    start = dt.datetime.today()-dt.timedelta(delta)
    end = dt.datetime.today()
    
    # looping over tickers and creating a dataframe with close prices
    for ticker in tickers:
        ohlc_mon[ticker] = yf.download(ticker,start,end,interval)
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
    data = returns(tickers = tickers[:number], interval = '1d', delta = 3650)
    print(data.shape)
    data.to_csv('changedata.csv',date_format='%Y-%m-%d')
    return data.shape
    
    