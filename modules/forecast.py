import warnings
import itertools
import numpy as np
import matplotlib.pyplot as plt
warnings.filterwarnings("ignore")
import statsmodels.api as sm
import os
import seaborn as sns
sns.set_style('whitegrid')
from pyramid.arima import auto_arima
import statsmodels.api as sm
from fbprophet import Prophet
from statsmodels.sandbox.regression.predstd import wls_prediction_std
import pandas as pd

from keras.models import Sequential
from keras.layers.recurrent import LSTM
from keras.layers.core import Dense, Activation, Dropout
from sklearn.metrics import mean_squared_error
from sklearn.utils import shuffle

from basic import rmse

# -----------  Forecasting Models  -----------

def auto_arimax(X, test_split = 0.2):
    # Do : data['Date'] = data['Date'].astype('datetime64[ns]')
    # data.set_index("Date", inplace = True)
    # Before sending data. The x axis labels wont get plotted  if not done.
    # plt.imsave() outside this function to save plot

    test_samples = int(X.shape[0] * test_split)
    train_data, test_data = X[:-test_samples], X[-test_samples:]
    train_data.columns = ["Training Data"]
    test_data.columns = ["Test Data"]

    stepwise_model = auto_arima(X, start_p=1, start_q=1,max_p=3, max_q=3, m=12,start_P=0, seasonal=True,d=1, D=1, trace=True,error_action='ignore',suppress_warnings=True,stepwise=True)
    stepwise_model.fit(train_data)

    predictions = stepwise_model.predict(n_periods = len(test_data))
    predictions = pd.DataFrame(predictions,index = test_data.index,columns=['Prediction'])
    result = pd.concat([train_data, test_data, predictions], axis = 1)
    result.plot()
    
    return rmse(np.array(test_data).flatten(), np.array(predictions).flatten())


def shallow_lstm(X):

	store_data = X
	x_test = X["2017"]
	X = X["2016"]
	look_back = 1

	def create_dataset(dataset, look_back=1):
		dataX, dataY = [], []
		for i in range(len(dataset)-look_back-1):
			a = dataset[i:(i+look_back)]
			dataX.append(a)
			dataY.append(dataset[i + look_back])
		return np.array(dataX), np.array(dataY)

	data = X.Close.values
	x, y = create_dataset(data)
	x_t, y_t = create_dataset(x_test.Close.values)

	trainX = np.reshape(x, (x.shape[0], 1, x.shape[1]))
	testX = np.reshape(x_t, (x_t.shape[0], 1, x_t.shape[1]))

	model = Sequential()
	model.add(LSTM(4, input_shape=(1, look_back)))
	model.add(Dense(1))
	model.compile(loss='mean_squared_error', optimizer='adam')
	model.fit(trainX, y, epochs=50, batch_size=1, verbose=2)

	trainPredict = model.predict(trainX)
	testPredict = model.predict(testX)
	# print(testPredict)
    
	predictions = pd.DataFrame(testPredict, index = x_test.index[:-2])
	results = pd.concat([store_data, predictions], axis = 1)
	results.columns = ["Train + Test", "Predictions"]    
	results.plot()
	
	return rmse(np.array(testX).flatten(), np.array(testPredict).flatten())


def prophet(X):
	# Pass DataFrame with data from 2016 i,e data["2016": ]
	# Use plt.imsave() outside function
	
	X = data["2016":]
	X.reset_index(inplace=True)
	X['Date'] = X['Date'].astype('datetime64[ns]')
	X.set_index("Date", inplace=True)

	train_data = X["2016"]
	test_data = X["2017":]
	test_data.reset_index(inplace=True)
	test_data['Date'] = test_data['Date'].astype('datetime64[ns]')
	test_data.set_index("Date", inplace=True)
	model = Prophet(yearly_seasonality=True, seasonality_prior_scale=0.1)

	model_data = pd.DataFrame(train_data.Close, train_data.index.values)
	model_data.reset_index(inplace=True)
	model_data.columns = ["ds", "y"]
	model.fit(model_data)

	future = model.make_future_dataframe(periods=int(len(test_data) + 100))
	forecast = model.predict(future)

	figure = model.plot(forecast)
	# forecast.yhat.plot()
	# result = pd.concat([X.Close, forecast.yhat], axis = 1)
	test_data.Close.plot(color = 'r', label="Test Data")
	plt.legend()

	return rmse(np.array(forecast[-len(test_data):].yhat), test_data.Close)

def regression_model(X):
	# Send data frame with only one column "Date" and the index set as date.
	# Date from 2016 to the end of the datasets
	data = X.reset_index()
	data['Date'] = data['Date'].astype('datetime64[ns]')
	data.set_index("Date", inplace=True)
	test_data = data["2017"]
	train_data = data["2016"]
	test_data.reset_index(inplace=True)
	train_data.reset_index(inplace=True)

	model = sm.GLSAR(train_data.Close, train_data.index.values, 50)
	results = model.fit()
	predictions = results.predict(list(range(len(train_data) + len(test_data))))
	test_data.set_index("Date", inplace=True)
	train_data.set_index("Date", inplace=True)
	predictions = pd.DataFrame(predictions, index=data["2016":].index)
	merged = pd.concat([train_data.Close, test_data.Close, predictions], axis = 1)
	merged.columns = ["Train Data", "Test Data", "Fitted Values"]
	merged.plot()
	return rmse(np.array(test_data.Close), np.array(predictions[-len(test_data):]).flatten())

# data = pd.read_csv("../Stocks/goog.us.txt")
# data['Date'] = data['Date'].astype('datetime64[ns]')
# data.set_index("Date", inplace = True)
# print(auto_arimax(data["2016":"2017"]["Close"]))
# plt.show()



