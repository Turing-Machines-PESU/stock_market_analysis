import os
import csv
import pandas as pd

path="../datasets/Companies/"
companies=[]
for file in os.listdir(path):
    if file[0]!='.':
        companies.append(file.split('.')[0].upper())

columnTitleRow = ['Symbol','Name','LastSale','MearketCap','IPOyear','Sector','industry','Summary Quote']
with open("stocks.csv", 'a',newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=columnTitleRow)
    writer.writeheader()

path_comp="../Stocks/"
with open("../datasets/filtered_companies.csv", 'a',newline='') as csvfile:
    writer = csv.writer(csvfile)
    for file in os.listdir(path_comp):
        if file[0]!='.':
            data=pd.read_csv(path_comp+file)
            for index, line in data.iterrows():
                if line["Symbol"] in companies:
                    writer.writerow(line[:-1])

