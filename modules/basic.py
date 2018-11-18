import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
import random

from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.filters.bk_filter import bkfilter
from statsmodels.tsa.filters import *
from statsmodels.tsa.filters.hp_filter import hpfilter
from statsmodels.tsa.stattools import grangercausalitytests
from statsmodels.tsa.stattools import kpss
from statsmodels.tsa.filters.cf_filter import cffilter
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from statsmodels.tsa.holtwinters import SimpleExpSmoothing

from datetime import date, timedelta
import datetime
# -----------  Utility Functions  -----------

def rmse(data1, data2):
	#data1 and data2 are numpy arrays
	if len(data1) == len(data2):
		return math.sqrt(sum((np.array(data1) - np.array(data2))**2)/len(data1))
	else:
		min_len = min([len(data1), len(data2)])
		return math.sqrt(sum((np.array(data1[min_len:]) - np.array(data2[min_len:]))**2)/min_len)

def rolling_rmse(data1, data2, window = 3):
	rolling_1 = data1.rolling(window)
	rolling_2 = data2.rolling(window)

def generte_dates(start, end, length):
	d1 = datetime.datetime.strptime(start, "%Y-%m-%d").date()
	d2 = datetime.datetime.strptime(end, "%Y-%m-%d").date()

	date_list = map(str, [d1 + timedelta(days=x) for x in range(0, (d2-d1).days + 1, 1)])
	if length > len(date_list):
		print("Date generation not possible")
	else:
		return random.choice(date_list, size = length, replace= False)

def impute_points(dataFrame, required_dates):
	# dataFrame : data frame with index = datetime and one column "Close"
	# required_dates : required dates in list of string
	
	new_data = pd.DataFrame(np.nan, index=required_dates, columns = ["Close"])
	new_data.reset_index(inplace=True)
	new_data.columns = ["Date", "Close"]
	new_data['Date'] = new_data['Date'].astype('datetime64[ns]')
	new_data.set_index("Date", inplace=True)

	new_data.update(dataFrame, overwrite = False)

	new_data = new_data.interpolate(method = 'time', order = 4)
	new_data.fillna(new_data.Close.mean(), inplace = True)

	return new_data



	
# -----------  Stationarity Tests  -----------


def aDickeyFuller(X):
	# Test for Stationarity
	result = adfuller(X, regression = 'ct')

	output = {}
	output["ADF Statistics"] = result[0]
	output["p value"] = result[1]
	output["Number of Lags Used"] = result[2]
	output["Critical values"] = result[4]

	return output

def kpss_test(X):
	# Test for Stationarity
	result = kpss(X, regression = 'ct')
	output = {}

	output["KPSS Statistics"] = result[0]
	output["p value"] = result[1]
	output["Number of Lags Used"] = result[2]
	output["Critical values"] = result[3]

	return output

# -----------  Smoothing Techniques  -----------

def exp_smoothing(data):
	model = ExponentialSmoothing(data, trend = "additive").fit(smoothing_level=0.1,optimized=True)
	result = model.fittedvalues
	return pd.DataFrame(result)

def simple_exp_smoothing(data):
	model = SimpleExpSmoothing(data).fit(smoothing_level = 0.1, optimized = True)
	result = model.fittedvalues
	return pd.DataFrame(result)


def moving_average(data, window = 8):
	#Left tailed
	rolling = data.rolling(window = window)
	result = rolling.mean()
	return pd.DataFrame(result)


# -----------  Filters  -----------

def  baxter_king(X, low = 10, high = 100, Lag = 20):
	# filter : Centers around zero
	cycle = bkfilter(X, low = low, high = high, K = Lag)
	return pd.DataFrame(cycle)


def hodrick_prescott(X, lamda = 6.5):
	# Filter : Centers around zero
	cycle, trend = hpfilter(X, lamda)
	return cycle

def random_walk_filter(X, low = 50, high = 300, drift = True):
	# Filter : Centers around zero
	
	cycle, trend = cffilter(X, low = low, high = high, drift = drift)
	return cycle


# -----------  Causality Test  -----------

def granger_test(data, maxlag = 50):
	# Test for granger causality
	result_granger = grangercausalitytests(data, maxlag = maxlag)
	return result_granger



