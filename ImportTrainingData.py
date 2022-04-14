import pandas as pd


X_train = pd.read_csv('data/trainingdata/x_train.csv')
X_test = pd.read_csv('data/trainingdata/x_test.csv')
y_train = pd.read_csv('data/trainingdata/y_train.csv')
y_test = pd.read_csv('data/trainingdata/y_test.csv')

X_train = X_train.drop(columns = ["Date"])
X_test = X_test.drop(columns = ["Date"])
y_train = y_train.drop(columns = ["Date"])
y_test = y_test.drop(columns = ["Date"])