import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import random
import time
import datetime
import seaborn as sns
from decimal import *
from wordcloud import WordCloud
import pylab
from collections import OrderedDict, defaultdict

data=pd.read_csv("../dataset/stocks.csv")
pd.options.mode.chained_assignment = None


#BoxPlot

print('Boxplot of Sectors')
market = data.dropna(subset=['MarketCap'])
market['MarketCap']=market['MarketCap'].apply(lambda x:float(str(x)[1:-1])*100 if x[-1]=='B' else float(str(x)[1:-1]))
sector1=market.loc[market['Sector']=='Transportation']
sector2=market.loc[market['Sector']=='Capital Goods']
sector3=market.loc[market['Sector']=='Consumer Non-Durables']
sector4=market.loc[market['Sector']=='Consumer Durables']
plt.figure(figsize=(8,15))
pylab.boxplot([sector1['MarketCap'],sector2['MarketCap'],sector3['MarketCap'],sector4['MarketCap']])
plt.xticks([1,2,3,4],['Transportation','Capital Goods','Consumer Durables','Consumer Non-Durables'],rotation=40)
plt.ylabel('Market Cap in Millions',fontsize=12)
plt.show()

print("Top 5 companies with highest MarketCap in Millions")
company=market.groupby(['Name'])['MarketCap'].sum()
company.sort_values(ascending=False).head(5)

#Histogram

lastsale=data.dropna(subset=['LastSale'])
plt.figure(figsize = (10, 7))
plt.hist(lastsale['LastSale'], bins=[2*i for i in range(100)],rwidth=0.9,color='green')
plt.xlabel('Last Sale', fontsize=15)
plt.ylabel('Frequency', fontsize=15)
plt.title('Distribution of Last Sale among companies',fontsize=25)
plt.show()

#WordCloud

comment_words = ' '
unwanted_words=['Services','Componets','Trusts','nan','Major','banks','service',"business",'substances']
print('Popular Industries')
for val in data.industry: 
      
    val = str(val) 
  
    tokens = val.split() 
      
    for i in range(len(tokens)): 
        tokens[i] = tokens[i].lower() 
          
    for words in tokens: 
        comment_words = comment_words + words + ' '
  
  
wordcloud = WordCloud(width = 800, height = 800, 
                background_color ='white', 
                stopwords = unwanted_words, 
                min_font_size = 10).generate(comment_words) 
                         
plt.figure(figsize = (5, 5), facecolor = None) 
plt.imshow(wordcloud) 
plt.axis("off") 
plt.tight_layout(pad = 0) 
plt.show() 


#BarGraph


market = data.dropna(subset=['MarketCap'])
market['MarketCap']=market['MarketCap'].apply(lambda x:float(str(x)[1:-1])*100 if x[-1]=='B' else float(str(x)[1:-1]))
mar=market.groupby(['Sector'])['MarketCap'].sum()
index = np.arange(len(mar.keys()))
plt.figure(figsize = (10,7))
plt.bar(index, mar[:])
plt.xlabel('Sectors', fontsize=15)
plt.ylabel('Currency in Millions', fontsize=15)
plt.xticks(index, mar.keys(), fontsize=12, rotation=45)
plt.title('Domination of MarketCap from various sector',fontsize=25)
plt.show()

#PieChart


print('Distribution of sectors')
mar=market.groupby(['Sector'])['MarketCap'].count()
plt.pie(mar[:],labels=mar.keys(),autopct='%1.1f%%',startangle=340)
plt.show()

