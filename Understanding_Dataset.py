
# coding: utf-8

# In[2]:

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import random
import time
import datetime
import seaborn as sns
# from pandas.tools.plotting import autocorrelation_plot
from pandas.plotting import autocorrelation_plot
sns.set(style="darkgrid")
get_ipython().magic('matplotlib inline')


# In[3]:

PATH = "Stocks/"
files = os.listdir(PATH)
print("Total Number of Companies: %d"%(len(files)))


# In[4]:

companies_9 = random.sample(files, 9)


# In[5]:

companies_9
data = []


# In[6]:

for file in companies_9:
    data.append(pd.read_csv(PATH + file))
    


# In[189]:

for item,company in zip(data,companies_9):
    print(company.split(".")[0])
    print(item.head())
    print("=========")


# In[190]:

for item,company in zip(data,companies_9):
    print(company.split(".")[0])
    print(item.describe())
    print("=========")


# In[191]:

for item,company in zip(data,companies_9):
    print(company.split('.')[0])
    plt.title("Company:  " + company.split('.')[0])
    print(item.corr())
    sns.heatmap(item.corr(), linewidths= 0.5, annot= True)
    plt.show()
    print("================")


# In[192]:

for item,company in zip(data,companies_9):
    print(company.split('.')[0])
    sns.pairplot(item)
    plt.title("Company:  " + company.split('.')[0])
    plt.show()
    print("===========")


#     OpenInt Seems to zero is most of the codes. We can safely ignore.

# In[142]:

for i in range(len(data)):
    data[i].drop(['OpenInt'],axis = 1, inplace = True)
    data[i].Date = pd.to_datetime(data[i].Date)


# In[143]:

data[0].columns


# In[144]:

type(data[0])


# In[145]:

# Opening Prizes
for name,i,company in zip(companies_9,range(1,10), data):
    plt.figure(figsize = (90,30))
    plt.subplot(3,3,i)
    plt.hist(company.Open,bins = range(int(company.Open.min()) - 1, int(company.Open.max())+1), normed = True, rwidth = 1)
    plt.xticks(range(int(company.Open.min()) - 1, int(company.Open.max())+1))
    plt.xlabel("Opening Value")
    plt.ylabel("Probability")
    plt.title("Company:  " + name.split(".")[0], fontsize = 20)
plt.show()


# In[146]:

# Closing Prices
for name,i,company in zip(companies_9,range(1,10), data):
    plt.figure(figsize = (90,30))
    plt.subplot(3,3,i)
    plt.hist(company.Close,bins = range(int(company.Close.min()) - 1, int(company.Close.max())+1), normed = True, rwidth = 1)
    plt.xticks(range(int(company.Close.min()) - 1, int(company.Close.max())+1))
    plt.xlabel("Closing Value")
    plt.ylabel("Probability")
    plt.title("Company:  " + name.split(".")[0], fontsize = 20)
plt.show()


# In[147]:

# Max Prices Reached for the day
for name,i,company in zip(companies_9,range(1,10), data):
    plt.figure(figsize = (90,30))
    plt.subplot(3,3,i)
    plt.hist(company.High,bins = range(int(company.High.min()) - 1, int(company.High.max())+1), normed = True, rwidth = 1)
    plt.xticks(range(int(company.High.min()) - 1, int(company.High.max())+1))
    plt.xlabel("Highest Prize for each day")
    plt.ylabel("Probability")
    plt.title("Company:  " + name.split(".")[0], fontsize = 20)
plt.show()


# In[ ]:




# In[148]:

# Lowest Value Reached for the day
for name,i,company in zip(companies_9,range(1,10), data):
    plt.figure(figsize = (90,30))
    plt.subplot(3,3,i)
    plt.hist(company.Low,bins = range(int(company.Low.min()) - 1, int(company.Low.max())+1), normed = True, rwidth = 1)
    plt.xticks(range(int(company.Low.min()) - 1, int(company.Low.max())+1))
    plt.xlabel("Lowest Prize for each day")
    plt.ylabel("Probability")
    plt.title("Company:  " + name.split(".")[0], fontsize = 20)
plt.show()


# In[18]:

for name,i,company in zip(companies_9,range(9), data):
    plt.figure(figsize=(15,5))
    sns.lineplot(data = data[i], x ='Date',y = "Open" , label = "Opening Value")
    sns.lineplot(data = data[i], x ='Date',y = "Close" , label = "Closing Value")
    sns.lineplot(data = data[i], x ='Date',y = "High", label = "Highest Value Per Day" )
    sns.lineplot(data = data[i], x ='Date',y = "Low" , label = "Lowest Value Per Day")
    plt.legend()
    #plt.xticks([])
    plt.xlabel("Time")
    plt.ylabel("Stock Prices")
    plt.title("Compnay:  " + name.split(".")[0])
    plt.show()


# In[23]:

for name,i,company in zip(companies_9,range(9), data):
    if(len(data[i].High) > 700):
            sns.swarmplot(y = random.sample(list(data[i].High), int(len(data[i].High) * 0.6)))
    else:
        sns.swarmplot(data = data[i], y = "High")
    plt.xlabel("Company:  " + name.split(".")[0])
    plt.show()


# In[85]:

get_ipython().magic('matplotlib inline')
ax = 0
plt.figure(figsize=(20,15))
for name,i,company in zip(companies_9,range(9), data):
    if not ax:
        ax = autocorrelation_plot(company.High, label = name.split(".")[0])
    else:
        ax = autocorrelation_plot(company.High, label = name.split(".")[0],ax= ax)
plt.legend(loc= 'best')
plt.title("AutoCorrelation Plot")
plt.show()


# In[7]:

ALL_PATH = "./stocks.csv"
data_all = pd.read_csv(ALL_PATH)


# In[8]:

data_all.head(50)


# In[9]:

data_all.describe()


# In[10]:

sns.heatmap(data_all.corr(),linewidths= 0.5, annot= True)


# In[17]:

choosen_names = random.sample(files, 5)
for i in range(len(choosen_names)):
    choosen_names[i] = choosen_names[i].split(".")[0]


# In[18]:

filtered_data = data_all.loc[~data_all['Company'].isin(choosen_names)]


# In[19]:

filtered_data.head()


# In[ ]:

sns.swarmplot(data = filtered_data, x = "Company", y = "High")


# In[ ]:



