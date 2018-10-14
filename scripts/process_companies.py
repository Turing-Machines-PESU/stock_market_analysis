import pandas as pd 
import os

PATH = "../datasets/Companies/"
STOCK_PATH = "../Stocks/"
companies = []

data_frames = []

for file in os.listdir(STOCK_PATH):
	companies.append(file.split(".")[0].upper())

for file in os.listdir(PATH):
	data = pd.read_csv(PATH + file)
	data_frames.append(data)

result = data_frames[0].append(data_frames[1:])

import pdb

output = result[result['Symbol'].isin(companies)]
# pdb.set_trace()
output.drop(output.columns[-1], axis = 1, inplace = True)
output.to_csv("../datasets/filtered_companies.csv", index = False)