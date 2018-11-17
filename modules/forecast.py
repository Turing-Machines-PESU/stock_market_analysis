import warnings
import itertools
import numpy as np
import matplotlib.pyplot as plt
warnings.filterwarnings("ignore")
import pandas as pd
import statsmodels.api as sm
import matplotlib
import os
import seaborn as sns
sns.set_style('whitegrid')
from pyramid.arima import auto_arima
import statsmodels.api as sm
import visualize as vs
import stock_data as sd

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
	train_data.rename("Train")
	train_data.rename("Test")

	stepwise_model = auto_arima(X, start_p=1, start_q=1,max_p=3, max_q=3, m=12,start_P=0, seasonal=True,d=1, D=1, trace=True,error_action='ignore',suppress_warnings=True,stepwise=True)
	stepwise_model.fit(train_data)

	predictions = stepwise_model.predict(n_periods = len(test_data))
	predictions = pd.DataFrame(predictions,index = test_data.index,columns=['Prediction'])
	result = pd.concat([train_data, test_data, predictions], axis = 1)
	result.plot()

	return rmse(pd.DataFrame(test_data), pd.DataFrame(predictions))


def shallow_lstm(X, test_split = 0.2):
	X['Item'] = pd.Series(list(range(len(X))))
	test_samples = int(X.shape[0] * test_split)
	train_data, test_data = X[:-test_samples], X[-test_samples:]

	# Yet to implement


	



# data = pd.read_csv("../Stocks/goog.us.txt")
# data['Date'] = data['Date'].astype('datetime64[ns]')
# data.set_index("Date", inplace = True)
# print(auto_arimax(data["2016":"2017"]["Close"]))
# plt.show()



