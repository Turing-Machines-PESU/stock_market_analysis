import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.filters.bk_filter import bkfilter
from statsmodels.tsa.filters import *
from statsmodels.tsa.filters.hp_filter import hpfilter
from statsmodels.tsa.stattools import grangercausalitytests
from statsmodels.tsa.stattools import kpss
from statsmodels.tsa.filters.cf_filter import cffilter
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from statsmodels.tsa.holtwinters import SimpleExpSmoothing


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
	output["Critical values"] = result[4]

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


def prepare_data_granger(dataFrame1, dataFrame2):
	# Data Frame 1 and Data Frame 2 are raw data frames
	dataFrame1.set_index("Date", inplace = True)
	dataFrame2.set_index("Date", inplace = True)
	data = pd.concat([dataFrame1["2016": "2017"].Close, dataFrame2["2016": "2017"].Close], axis = 1)
	return data

def granger_test(data, maxlag = 50):
	# Test for granger causality
	result_granger = grangercausalitytests(data, maxlag = maxlag)
	return result_granger



