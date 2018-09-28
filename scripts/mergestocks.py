import os
import csv

# Open a file
path = "../datasets/"

# This would print all the files and directories
columnTitleRow = ['Company','Date','Open','High','Low','Close','Volume','OpenInt']
with open("../datasets/stocks.csv", 'a',newline='') as csvfile:
		writer = csv.DictWriter(csvfile, fieldnames=columnTitleRow)
		writer.writeheader()
for file in os.listdir(path):
	
	with open("../datasets/"+file, 'r') as in_file:
	   	try:
	   		next(in_file)
		   	stripped = [line.strip() for line in in_file]
		   	lines = [line.split(",") for line in stripped if line]
		   	comp = file.split(".")[0]
		   	for line in lines:
		   		line.insert(0,comp)
		   	
		   	with open("../datasets/stocks.csv", "a", newline='') as f:
		   		writer = csv.writer(f)
		   		writer.writerows(lines)
	   	except:
	   		pass
			
