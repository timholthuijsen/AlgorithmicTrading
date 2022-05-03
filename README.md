# Algorithmic Trading
### A repository for building a stock trading algorithm using machine learning and deep learning

This repository contains my collected work in building an algorithm that can predict stock prices using Keras Neural Networks and Sklearn machine learning algorithms. 
Many files for predicing future price changes and patterns, obtaining and tranforming training data, and eventually buying and selling selected stocks are included in this repository.

In order to add some structure to the files, a file map is included, explaining the function and purpose of each file in the repository.
<br>

## File map

### Models

- LSTM.ipynb

The development of a Long Short-Term Memory (LSTM) Neural Network model used for stock-price prediction. 
This model currently seems like the most skillful option for price pattern recognition. Further optimization of the model is underway.

- RandomForestRegression.py

A function using a Random Forest Regressor from sklearn to predict future price changes. Shows large promise.

- RenkoMacd.py

A function using a Renko Macd algorithmic trading approach to find optimal stock buy and sell moments. A more common approach to algorithmic trading.

- VotingRegression.py

A combination of multiple regressor models used in a voting model. Show promise for accurate price predictions. Consider implementing LSTM into the vote.

<br>

### Helper functions

- Trading.py

A function used to buy and sell chosen stocks using the Alpaca Trading API

- TrainingDataGeneration.py

A function used to generate data that can be used to train Ai models

- ImportTrainingData.py

A helper function used to easily import training data into another function

- LiveStream.py

A function for getting live stock-price updates

- HyperparameterTuning.py

A function used to tune and optimize the hyperparameters of a given machine learning model

<br>

### Data

- Stock_data.csv

A large file containing all relevant info about a specific stock, in this case Google. 
Can be generated for any specific stock using TrainingDataGeneration.py by simply changing the ticker variable

- Data

A folder used for storing all the data used to train and eveluate the models

- DownloadData.py

A function used to download stock data

- DerivativeDataDownloader.py

A function for downloading price change data rather than price data

- ReorganizingColumns.ipynb

A function used for reorganizing the columns of the training data 

<br>
<br>
<br>

For questions, comments, or additions, you can reach out to me at: timholthuijsen@hotmail.com
