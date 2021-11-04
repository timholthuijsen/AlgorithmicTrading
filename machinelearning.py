from sklearn.ensemble import RandomForestRegressor
from sklearn import metrics
import pandas as pd
from yfinance_multiple_tickers import *
import numpy as np
from buying import *


data = pd.read_csv("changedata.csv")

filleddata = data.fillna(0)

column_names = tickers
#Remove a couple of columns with infinite values
try:
    column_names.remove('JPST')
    column_names.remove('FLQL')
    column_names.remove('FLQS')
    column_names.remove('FLQM')
except:
    pass

train_columns = []
test_columns = []

#train/test split
counter = 0
for name in column_names:
    counter += 1
    if counter % 5 == 0:
        test_columns.append(name)
    else:
        train_columns.append(name)
        
    
    
#Create train and test data
xtrain = filleddata[:2514][train_columns]
ytrain = filleddata[2514:2515][train_columns]
xtest = filleddata[:2514][test_columns]
ytest = filleddata[2514:2515][test_columns]

#transpose to turn dates into seperate features (historic data)
xtrain = xtrain.transpose()
ytrain = ytrain.transpose()
xtest = xtest.transpose()
ytest = ytest.transpose()
ytest.rename(columns = {2514:'change'})
ytrain.rename(columns = {2514:'change'})
    
    
    

#Training the model and let it make predictions

model = RandomForestRegressor(random_state = 42)
model.fit(xtrain, ytrain)
predictions = model.predict(xtest)



#test how accurate the model is
def compare():
    #accuracy measurements
    print('Mean Absolute Error:', metrics.mean_absolute_error(ytest, predictions))
    print('Mean Squared Error:', metrics.mean_squared_error(ytest, predictions))
    print('Root Mean Squared Error:', np.sqrt(metrics.mean_squared_error(ytest, predictions)))
    
    #Create a dumb predictor to compare skillfullness:
    dumb = np.zeros(104)
    #Test it on the same accuracy measures
    print('Mean Absolute Error of the dumb predictor:', metrics.mean_absolute_error(ytest, dumb))
    print('Mean Squared Error of the dumb predictor:', metrics.mean_squared_error(ytest, dumb))
    print('Root Mean Squared Error of the dumb predictor:', np.sqrt(metrics.mean_squared_error(ytest, dumb)))
    
    #Creating a 'yesterday' predictor:
    yyesterday = xtest[2513]
    print('Mean Absolute Error of the yesterday predictor:', metrics.mean_absolute_error(ytest, yyesterday))
    print('Mean Squared Error of the yesterday predictor:', metrics.mean_squared_error(ytest, yyesterday))
    print('Root Mean Squared Error of the yesterday predictor:', np.sqrt(metrics.mean_squared_error(ytest, yyesterday)))
#compare()



def predictor(time=2515, serious = False, qty = 1):  
    current = filleddata[1:time][column_names].transpose()
    today = model.predict(current)
    profits = {}
    for name, profit in zip(column_names,today):
        profits[name] = profit
    max_key = max(profits, key = profits.get)
    max_value = profits[max_key]
    print('the model predicts that ', max_key, "is going to increase by ", max_value, ' today')
    print('we should buy ',max_key, ' now!')
    if serious:
        buy_order(max_key,qty,'market','gtc')
        
    return profits

predictor()




    

    