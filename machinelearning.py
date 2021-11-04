from sklearn.ensemble import RandomForestRegressor
from sklearn import metrics
import pandas as pd
from yfinance_multiple_tickers import *
import numpy as np
from buying import *
from Trading import *


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



def predictor(time=2515, serious = False):  
    #Get modern data
    current = filleddata[1:time][column_names].transpose()
    #predict values for today
    today = model.predict(current)
    profits = {}
    #get them all in a dict
    for name, profit in zip(column_names,today):
        profits[name] = profit
    #get the highest key and value
    max_key = max(profits, key = profits.get)
    max_value = profits[max_key]
    print('the model predicts that ', max_key, "is going to increase by ", max_value, ' today')
    print('we should buy ',max_key, '!!')
    #start buying highest key
    if serious:
        proceed = input("Do you wish to buy this stock now?  (yes/no) ")
        if proceed == 'yes':
            qty = int(input("how many do you wish to buy? "))
            if isinstance(qty, int):
                print('attempting to buy ',qty,' ', max_key)
                buy_order(max_key,qty,'market','gtc')
    if serious == False:
        return profits


#buy a num of the best stocks
def buy_best(num_of_stocks, qty = 1):
    print('We want to buy the best ', num_of_stocks, ' stocks')
    prediction = predictor()
    worthystocks = []
    for i in range(num_of_stocks):
        max_key = max(prediction, key = prediction.get)
        max_value = prediction[max_key]
        print(max_key, ' is expected to rise ',max_value, ' today')
        worthystocks.append(max_key)
        del(prediction[max_key])
    print('worthy stocks are: ', worthystocks)
    buyer(worthystocks, qty)
    




    

    