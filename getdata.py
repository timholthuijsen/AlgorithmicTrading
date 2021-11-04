import time
from datetime import datetime
from yfinance_multiple_tickers import *
from buying import *


#live price updates and sends a signal when goal is met
def get_live_price(tickers, goal = 1000000, 
                   continuous = True, refresh = 5):
    while continuous:
        for ticker in tickers:
            live_price = pd.DataFrame()
            live_price[ticker] = yf.download(ticker, period='5m',interval='1m')['Adj Close']
            price_data = live_price.iloc[-1]
            for item in price_data:
                price = item
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            print(ticker, 'at', current_time,'Price: ', price)
            #keep it live refreshed
            if price > goal:
                refresh = 0.1
                continuous = False
            time.sleep(refresh)
            
    #exit while-loop when goal is met        
    print(ticker, 'Loop exited at', current_time,
          'Price: ', price)
    signal = 'sell'
    return signal

def live_sells(ticker, goal,qty, refresh = 5):
    result = get_live_price(ticker, goal, refresh)
    if result == 'sell':
        print('WE SHOULD SELL NOW!')


#get_live_price('BLDP', refresh = 2)



