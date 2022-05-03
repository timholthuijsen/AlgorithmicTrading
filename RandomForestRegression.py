import pandas as pd
from sklearn.svm import SVC
import ImportTrainingData
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import classification_report
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error


x_train = ImportTrainingData.X_train
x_test = ImportTrainingData.X_test
y_train = ImportTrainingData.y_train
y_test = ImportTrainingData.y_test


y_train = y_train.ravel()
y_test = y_test.ravel()

#Define and train the model
model =RandomForestRegressor(n_estimators=1000, max_features=8, random_state=42, verbose = 0, n_jobs = -1)
model.fit(x_train,y_train)

predictions = model.predict(x_test)

 

mse = mean_squared_error(y_test, predictions)

print(f'mean squared error of the model is {mse}')