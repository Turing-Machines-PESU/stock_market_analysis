import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import adfuller

def aDickeyFuller(X):
	result = adfuller(X, regression = 'ct')

	output = {}
	output["ADF Statistics"] = result[0]
	output["p value"] = result[1]
	output["Number of Lags Used"] = result[2]
	output["Critical values"] = result[4]

	return output 
