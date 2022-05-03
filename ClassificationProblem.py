"""
The idea of this function is that rather than attempting to predict the
exact value that a stock will take, we simply try to predict whether it will 
rise or fall. With this approach, we can hopefully gain a higher accuracy in
determining which stocks are worthwhile to buy. 
We train a number of different Classifiers and determine their accuracy:
"""

from sklearn.ensemble import RandomForestClassifier
import ImportTrainingData
import pandas as pd
from sklearn.neural_network import MLPClassifier
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.datasets import make_moons, make_circles, make_classification
from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.gaussian_process.kernels import RBF
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis



x_train = ImportTrainingData.X_train
x_test = ImportTrainingData.X_test
y_train = ImportTrainingData.y_train_dummy
y_test = ImportTrainingData.y_test_dummy


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

def run_models(classifiers):
    accuracies = []
    models = []
    for model in classifiers:
        print('trying', model)
        model.fit(x_train,y_train)
        prediction=model.predict(x_test)
        accuracy = classifier_test(predicted=prediction, real = y_test)
        accuracies.append(accuracy)

        
classifiers = [
    KNeighborsClassifier(3),
    SVC(kernel="linear", C=0.025),
    SVC(gamma=2, C=1, probability = True),
    GaussianProcessClassifier(1.0 * RBF(1.0)),
    DecisionTreeClassifier(max_depth=5),
    RandomForestClassifier(max_depth=5, n_estimators=10, max_features=1),
    MLPClassifier(alpha=1, max_iter=1000),
    AdaBoostClassifier(),
    GaussianNB(),
    QuadraticDiscriminantAnalysis(),
]

run_models(classifiers=classifiers)
    
    
# classifier_test(predicted = prediction, real = y_test)


# Make a random dataset:
height = [38, 55, 61, 38, 41,54,61,38,38,61]
bars = ('Kneighbors', 'SVC', 'SVC2', 'Gaussian', 'DecisionTree','RandomForest','MLP','Adaboost','GaussianNB','QDA')
y_pos = np.arange(len(bars))

# Create bars
plt.bar(y_pos, height)

# Create names on the x-axis
plt.xticks(y_pos, bars)

# Show graphic
plt.show()
