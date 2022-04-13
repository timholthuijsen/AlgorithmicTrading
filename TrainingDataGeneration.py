import yfinance as yf
import talib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

ticker= "googl"
#For long term, large interval:
stock_data = yf.download(ticker, start="2016-01-04", end="2021-05-12")
#For short term, small interval: 
# stock_data = yf.download(ticker, start = dt.datetime.today()-dt.timedelta(1800), end=dt.datetime.today(), interval='1d')

stock_data['Adj Close'].plot()
plt.ylabel("Adjusted Close Prices")
plt.show()

changes = stock_data['Adj Close'].pct_change()

feature_names = []
for n in [14, 30, 50, 200]:
    stock_data['ma' + str(n)] = talib.SMA(stock_data['Adj Close'].values, timeperiod=n)
    stock_data['rsi' + str(n)] = talib.RSI(stock_data['Adj Close'].values, timeperiod=n)

    feature_names = feature_names + ['ma' + str(n), 'rsi' + str(n)]
    

stock_data['Volume_1d_change'] = stock_data['Volume'].pct_change()

volume_features = ['Volume_1d_change']
feature_names.extend(volume_features)

#Append lag for timeseries analysis
for i in range(20):
    string = str(i)+"_lag"
    stock_data[string] = stock_data['Adj Close'].shift(i)
    feature_names = feature_names + [str(i) + '_lag']


stock_data['5d_future_close'] = stock_data['Adj Close'].shift(-5)
stock_data['5d_close_future_pct'] = stock_data['5d_future_close'].pct_change(5)



stock_data.dropna(inplace=True)

X = stock_data[feature_names]
y = stock_data['5d_close_future_pct']

train_size = int(0.85 * y.shape[0])
X_train = X[:train_size]
y_train = y[:train_size]
X_test = X[train_size:]
y_test = y[train_size:]

#Getting rid of inf values:
X_train = X_train.replace([np.inf, -np.inf], 0).dropna(axis=0)


def csv_writer(data, filename):
    data.to_csv(filename, date_format = '%Y-%m-%d')

csv_writer(X_train, 'data/trainingdata/x_train.csv')
csv_writer(y_train, 'data/trainingdata/y_train.csv')
csv_writer(X_test, 'data/trainingdata/x_test.csv')
csv_writer(y_test, 'data/trainingdata/y_test.csv')
