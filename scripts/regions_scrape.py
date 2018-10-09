from time import sleep
import re
import csv
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait
import calendar
import requests, zipfile, io
import platform



if platform.system() == "Windows":
	r = requests.get("https://chromedriver.storage.googleapis.com/2.42/chromedriver_win32.zip")
	z = zipfile.ZipFile(io.BytesIO(r.content))
	z.extractall()
elif platform.system() == "Linux":
	r = requests.get("https://chromedriver.storage.googleapis.com/2.42/chromedriver_linux64.zip")
	z = zipfile.ZipFile(io.BytesIO(r.content))
	z.extractall()
else:
	r = requests.get("https://chromedriver.storage.googleapis.com/2.42/chromedriver_mac64.zip")
	z = zipfile.ZipFile(io.BytesIO(r.content))
	z.extractall()

d = webdriver.Chrome()
base_url="https://trendogate.com/"
d.get(base_url)

select = Select(d.find_element_by_name('place'))
places=[o.text for o in select.options]
myString='United States'
pattern = r'\b' + re.escape(myString) + r'\b'
values = [x for i, x in enumerate(places) if re.search(pattern, x)]
print(values)

with open("../datasets/regions.csv", "w") as output:
    writer = csv.writer(output, lineterminator='\n')
    writer.writerow(['Regions'])
    for val in values:
        writer.writerow([val])   


