"""
The idea of this dataset is that rather than attempting to predict the
exact value that a stock will take, we simply try to predict whether it will 
rise or fall. With this approach, we can hopefully gain a higher accuracy in
determining which stocks are worthwhile to buy. 
"""

#work in progress

import pandas as pd

xtrain = pd.read_csv("data/trainingdata/x_train.csv")