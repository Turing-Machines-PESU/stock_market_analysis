import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.filters.bk_filter import bkfilter
from statsmodels.tsa.filters import *
from statsmodels.api.tsa.filters import hpfilter
from statsmodels.tsa.stattools import grangercausalitytests

def aDickeyFuller(X):
	result = adfuller(X, regression = 'ct')

	output = {}
	output["ADF Statistics"] = result[0]
	output["p value"] = result[1]
	output["Number of Lags Used"] = result[2]
	output["Critical values"] = result[4]

	return output

def  baxter_king(X, low = 5, high = 25, Lag = 4):
	result_bk = bkfilter(X, low = low, high = high, K = Lag)
	return pd.DataFrame(result_bk)

def hodrick_prescott(X, lamda = 6.5):
	_, result_hp = hpfilter(X, lamda)
	return result_hp

def prepare_data_granger(dataFrame1, dataFrame2):
	dataFrame1.set_index("Date", inplace = True)
	dataFrame2.set_index("Date", inplace = True)

	data = pd.concat([dataFrame1["2016": "2017"].Close, dataFrame2["2016": "2017"].Close], axis = 1)

	return data

def granger_test(data, maxlag = 50):
	result_granger = grangercausalitytests(data, maxlag = maxlag)

	return result_granger


