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



X_train = pd.read_csv('data/trainingdata/x_train.csv')
X_test = pd.read_csv('data/trainingdata/x_test.csv')
y_train = pd.read_csv('data/trainingdata/y_train.csv')
y_test = pd.read_csv('data/trainingdata/y_test.csv')

X_train = X_train.drop(columns = ["Date"])
X_test = X_test.drop(columns = ["Date"])
y_train = y_train.drop(columns = ["Date"])
y_test = y_test.drop(columns = ["Date"])


reg1 = GradientBoostingRegressor(random_state=1, verbose = 1)
reg2 = RandomForestRegressor(n_estimators=1000, max_features=8, random_state=42, verbose = 1, n_jobs = -1)
reg3 = AdaBoostRegressor()
rf_model = VotingRegressor(estimators=[('gb', reg1), ('rf', reg2), ('ad', reg3)])
# ereg.fit(X, y)

# rf_model = reg2






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


feature_names = []
for column in X_train:
    feature_names.append(column)

# Commenting out feature importances in order to run voting regressor:
# importances = rf_model.feature_importances_
# sorted_index = np.argsort(importances)[::-1]
# x_values = range(len(importances))
# labels = np.array(feature_names)[sorted_index]
# plt.figure(figsize=(20,20)) 
# plt.bar(x_values, importances[sorted_index], tick_label=labels)
# plt.xticks(rotation=90)
# plt.show()


predicted = rf_model.predict(X_test)

def simple_backtest(predicted):
    """ A simple backtest that tests whether the negative/postive values of the prediction line up"""
    results = []
    # predicted = rf_model.predict(X_test)
    real = y_test.to_numpy()
    for i in range(1,len(real)):
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
    