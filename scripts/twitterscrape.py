from time import sleep
import csv
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait
from datetime import timedelta, date

def daterange(start_date, end_date):
    for n in range(0,int ((end_date - start_date).days) + 1,7):
        yield start_date + timedelta(n)

start_date = date(2016, 12, 7)
end_date = date(2016, 12, 30)

with open('regions.csv') as csvfile:
    csvFile = csv.reader(csvfile,delimiter=",")
    places=[row[:-1] for row in csvfile]

print(places)
d = webdriver.Chrome()
base_url="https://trendogate.com/"
d.get(base_url)


columnTitleRow = ['Regions', 'Date', 'Hashtags']
with open("twitter.csv", 'a',newline='') as csvfile:
		writer = csv.DictWriter(csvfile, fieldnames=columnTitleRow)
		writer.writeheader()

try:

	for single_date in daterange(start_date, end_date):
		date_formated=single_date.strftime("%d-%m-%Y")
		for reg in places:
			d.find_element_by_xpath("//*[@id='userheaderbox']/div/form[2]/div[1]/select[@name='place']/option[text()='"+reg+"']").click()
			sleep(1)
			region=reg.split("/")[-1]
			d.find_element_by_xpath("//*[@id='userheaderbox']/div/form[2]/div[2]/input").send_keys(str(date_formated))
			sleep(1)
			d.find_element_by_xpath("//*[@id='userheaderbox']/div/form[2]/button[@type='submit']").click()	
			date= d.find_element_by_xpath("/html/body/div[4]/div/div[1]/div/h3").text.split(" ")[-1]	
			try:

				html_list = d.find_element_by_xpath("/html/body/div[4]/div/div[1]/div/ul")
				items = html_list.find_elements_by_tag_name("li")
				for item in items:
					try:
						csv_list=[]	
						text = item.text
						csv_list.append(region)
						csv_list.append(date)
						csv_list.append(text)
						print(csv_list) 
						with open("twitter.csv", "a") as output:
							writer = csv.writer(output, lineterminator='\n')
							writer.writerow(csv_list)
					except:
						pass  
				d.implicitly_wait(60)
			except:
				csv_list=[]	
				text = "NA"
				csv_list.append(region)
				csv_list.append(date)
				csv_list.append(text)
				print(csv_list) 
				with open("twitter.csv", "a") as output:
					writer = csv.writer(output, lineterminator='\n')
					writer.writerow(csv_list)

		d.refresh()	
except:
	d.back()

	
	


