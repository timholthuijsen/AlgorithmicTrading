import pandas as pd
from sklearn.preprocessing import StandardScaler


X_train = pd.read_csv('data/trainingdata/extensive_x_train.csv')
X_test = pd.read_csv('data/trainingdata/extensive_x_test.csv')
y_train = pd.read_csv('data/trainingdata/5d_y_train.csv')
y_test = pd.read_csv('data/trainingdata/5d_y_test.csv')
stock_data = pd.read_csv('data/trainingdata/stock_data.csv')

X_train = X_train.drop(columns = ["Date"])
X_test = X_test.drop(columns = ["Date"])
y_train = y_train.drop(columns = ["Date"])
y_test = y_test.drop(columns = ["Date"])



def make_dummy(dataset):
    for column in dataset:
        for index,value in enumerate(dataset[column]):
            if value > 0:
                dataset.loc[index] = 1
            if value <= 0:
                dataset.loc[index]=0
    return dataset

#transform data into dummies and right format
y_train_dummy = make_dummy(y_train).to_numpy().ravel()
y_test_dummy = make_dummy(y_test).to_numpy().ravel()

y_train = y_train.to_numpy()
y_test = y_test.to_numpy()

x_train = X_train.to_numpy()
x_test = X_test.to_numpy()

#and scale them with standard scaler
# x_train = StandardScaler().fit_transform(x_train)
# x_test = StandardScaler().fit_transform(x_test)