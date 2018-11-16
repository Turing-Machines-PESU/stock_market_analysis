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

def aDickeyFuller(X):
	# Test for stationality
	result = adfuller(X, regression = 'ct')

	output = {}
	output["ADF Statistics"] = result[0]
	output["p value"] = result[1]
	output["Number of Lags Used"] = result[2]
	output["Critical values"] = result[4]

	return output

def kpss_test(X):
	# Test for stationality
	result = kpss(X, regression = 'ct')
	output = {}

	output["KPSS Statistics"] = result[0]
	output["p value"] = result[1]
	output["Number of Lags Used"] = result[2]
	output["Critical values"] = result[4]

	return output


def  baxter_king(X, low = 10, high = 100, Lag = 20):
	# Smoothig filter : Centers around zero
	result_bk = bkfilter(X, low = low, high = high, K = Lag)
	return pd.DataFrame(result_bk)


def hodrick_prescott(X, lamda = 6.5):
	# Smoothig Filter : This does not center around zero
	_, result_hp = hpfilter(X, lamda)
	return result_hp

def random_walk_filter(X, low = 50, high = 300, drift = True):
	# Smoothing Filter : Centers around zero
	
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



