import pandas as pd
from sklearn.svm import SVC
import ImportTrainingData
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import classification_report
from sklearn.ensemble import RandomForestClassifier


x_train = ImportTrainingData.X_train
x_test = ImportTrainingData.X_test
y_train = ImportTrainingData.y_train_dummy
y_test = ImportTrainingData.y_test_dummy

#Define and train the model
model = RandomForestClassifier(max_depth=1, max_features='log2',
                       min_impurity_decrease=0, n_estimators=10, n_jobs=-1,
                       random_state=42, verbose=1)
model.fit(x_train,y_train)

predictions = model.predict(x_test)

 
# Doing some Grid search to optimize hyperparameters:
param_grid = {'max_depth': [None, 1, 5, 8, 10, 30, 50, 100],
              'n_estimators': [1, 10, 100, 200, 400, 1000, 2000],
              'max_features': [5,'auto','sqrt','log2'],
              'min_impurity_decrease': [0, 0.1, 0.3, 0.8]}
 

rfc = RandomForestClassifier(random_state = 42, n_jobs = -1, verbose = 1)
grid = GridSearchCV(rfc, param_grid, refit = True, verbose = 3)
# grid.fit(x_train, y_train)


def classifier_test(predicted, real):
    results = []
    for index, prediction in enumerate(predicted):
        if prediction == real[index]:
            results.append(1)
        else:
            results.append(0)
    accuracy = sum(results)/len(results) * 100
    print('accuracy is:', accuracy)
    return accuracy

# best_params = grid.best_params_
# best_estimators = grid.best_estimator_
# print('best parameters are:', best_params)

#and run a test on the accuracy
classifier_test(predictions, y_test)
print(classification_report(y_test, predictions))