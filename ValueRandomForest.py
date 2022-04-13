import yfinance as yf
import talib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import pyplot
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import ParameterGrid
from sklearn import metrics
import datetime as dt
from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.ensemble import AdaBoostRegressor
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import VotingRegressor


ticker= "googl"
# stock_data = yf.download(ticker, start="2016-01-04", end="2021-05-12")
stock_data = yf.download(ticker, start = dt.datetime.today()-dt.timedelta(50), end=dt.datetime.today(), interval='5m')
stock_data = stock_data.dropna(axis=0)

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
for i in range(40):
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
# X_train['Volume_1d_change'][397] = -0.5
y_train = y[:train_size]
X_test = X[train_size:]
y_test = y[train_size:]

#trying to get rid of inf values:
X_train = X_train.replace([np.inf, -np.inf], 0).dropna(axis=0)


grid = {'n_estimators': [200], 'max_depth': [3], 'max_features': [4, 8], 'random_state': [42]}
test_scores = []

rf_model = RandomForestRegressor()

for g in ParameterGrid(grid):
    rf_model.set_params(**g) 
    rf_model.fit(X_train, y_train)
    test_scores.append(rf_model.score(X_test, y_test))

best_index = np.argmax(test_scores)
print(test_scores[best_index], ParameterGrid(grid)[best_index])

reg1 = GradientBoostingRegressor(random_state=1, verbose = 1)
reg2 = RandomForestRegressor(n_estimators=1000, max_features=8, random_state=42, verbose = 1, n_jobs = -1)
reg3 = AdaBoostRegressor()
rf_model = VotingRegressor(estimators=[('gb', reg1), ('rf', reg2), ('ad', reg3)])
# ereg.fit(X, y)





# rf_model = AdaBoostRegressor()
# rf_model = GradientBoostingRegressor(n_estimators=100, learning_rate=0.1, max_depth=1, random_state=0)
# rf_model = RandomForestRegressor(n_estimators=200, max_depth=3, max_features=4, random_state=42)
rf_model.fit(X_train, y_train)

y_pred = rf_model.predict(X_test)

y_pred_series = pd.Series(y_pred, index=y_test.index)
y_pred_series.plot()
plt.ylabel("Predicted 5 Day Close Price Change Percent")
plt.show()



print('Mean Absolute Error:', metrics.mean_absolute_error(y_test, y_pred))
print('Mean Squared Error:', metrics.mean_squared_error(y_test, y_pred))
print('Root Mean Squared Error:', np.sqrt(metrics.mean_squared_error(y_test, y_pred)))


#Commenting out feature importances in order to run voting regressor:
# importances = rf_model.feature_importances_
# sorted_index = np.argsort(importances)[::-1]
# x_values = range(len(importances))
# labels = np.array(feature_names)[sorted_index]
# plt.bar(x_values, importances[sorted_index], tick_label=labels)
# plt.xticks(rotation=90)
# plt.show()


predicted = rf_model.predict(X_test)
def simple_backtest(predicted):
    """ A simple backtest that tests whether the negative/postive values of the prediction line up"""
    results = []
    # predicted = rf_model.predict(X_test)
    real = y_test
    for i in range(len(real)):
        if predicted[i] < 0 and real[i] < 0 or predicted[i] > 0 and real[i] > 0:
            results.append(True)
        else:
            results.append(False)
    length = len(results)
    corrects = sum(results)
    accuracy = 100 * corrects/length
    print(f'Out of {length} results, {corrects} were in the correct range')
    print(f'an accuracy of {accuracy} procent')
    return accuracy

simple_backtest(predicted = predicted)


def plot(testY, ypredicted):
    testarray = testY.to_numpy()
    plt.plot(testarray, label='True Value')
    plt.plot(ypredicted, label='Predicted Value')
    plt.title("Google Real vs Predicted change values")
    plt.legend()
    plt.show()

plot(testY = y_test, ypredicted = predicted)
    