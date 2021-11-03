# -*- coding: utf-8 -*-
"""
Created on Wed Nov  3 04:12:06 2021

@author: timho
"""

from buying import *
from yfinance_multiple_tickers import *


#calculate average prices of a stock
def average(ticker):
    global avg
    avg = cl_price[ticker].mean()
    global avgweek
    avgweek = cl_price[ticker][723:730].mean()
    global avgmonth
    avgmonth = cl_price[ticker][700:730].mean()
    global avgyear
    avgyear = cl_price[ticker][360:730].mean()
    
    
worthystocks = []
#Determine which stocks to buy according to certain criteria. WIP.
def checker(ticker):
    score = 0
    average(ticker)
    if cl_price[ticker][-1] < avg * 0.98:
        print(ticker + 'price is below total average')
        score += 1
    else:
        print(ticker + 'price is above total average')
        
    if cl_price[ticker][-1] < avgweek * 0.98:
        print(ticker + 'price is below week average')
        score += 1
    else:
        print(ticker + 'price is above week average')
        
    if cl_price[ticker][-1] < avgmonth * 0.98:
        print(ticker + 'price is below month average')
        score += 1
    else:
        print(ticker + 'price is above month average')
        
    if cl_price[ticker][-1] < avgyear * 0.98:
        print(ticker + 'price is below year average')
        score += 1
    else:
        print(ticker + 'price is above year average')
    print('score for' + ticker + 'is:' + str(score))
    if score >= 2:
        worthystocks.append(ticker)
        
#Investigate a number of stocks and, if applicable, dub them worthy
def processor(tickers,number):
    worthystocks = []
    tickers = tickers[:number]+stocks
    download(tickers, number)
    for ticker in tickers:
        try:
            checker(ticker)
        except KeyError:
            continue
    print(worthystocks)

#automatically buy all worthy stocks
def buyer(worthystocks):
    for ticker in worthystocks:
        current_price = cl_price[ticker][-1]
        stop = current_price *1.05
        loss = current_price * 0.5
        create_order(ticker, 1,'buy','market','gtc',stop,loss)
        print('bought 1 ' + ticker + 'for a price of ' + str(current_price))

#investigate stocks for worthiness and then buys them
def run():
    processor(tickers,20)
    buyer(worthystocks)
