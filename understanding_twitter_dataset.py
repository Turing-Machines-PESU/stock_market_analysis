
# coding: utf-8

# In[9]:


import pandas as pd
import random
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import plotly
import plotly.graph_objs as go
import numpy as np
import datetime
import calendar as cd
import seaborn as sns
sns.set(style="whitegrid")
import warnings
warnings.filterwarnings('ignore')


# In[10]:


twitter= pd.read_csv("./datasets/twitter.csv")
twitter['Hashtags'] = twitter.Hashtags.str.lower()
twitter.drop_duplicates(inplace=True)
twitter.reset_index(drop=True,inplace=True)


# In[11]:


twitter.describe()


# In[12]:


regions = pd.DataFrame({'Regions':pd.unique(twitter.Regions)})
regions=regions[regions.Regions!='United States']
regions_2 = random.sample(list(regions.Regions),2)
print("Regions:",regions_2)


# In[13]:


#Wordcloud of HashTags for a particular region
for reg in regions_2:
    reg_data = twitter[twitter['Regions']==reg]
    print(reg)
    grp_tags = pd.DataFrame({'freq' : reg_data.groupby(['Hashtags']).size()}).sort_values(by=['freq'],ascending=False).reset_index()
    top_50_tags=grp_tags.head(50)
    #top_10_tags['Hashtags']=pd.DataFrame(tag_list)
    print(top_50_tags.head(10))
    d = {}
    for tag, freq in grp_tags.values:
        d[tag] = freq
    wordcloud = WordCloud(
                          stopwords=STOPWORDS,
                          background_color='white',
                          width=4000,
                          height=3500
                         )
    wordcloud.generate_from_frequencies(frequencies=d)
    plt.figure(figsize = (10,10))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.show()
    
    print("===========")


# In[14]:


grp_data= pd.DataFrame({'freq' : twitter.groupby(['Date','Hashtags']).size()}).sort_values(by=['Date'],ascending=True).reset_index()
grp_entire_data= pd.DataFrame({'freq' : twitter.groupby(['Regions','Date','Hashtags']).size()}).sort_values(by=['Date'],ascending=True).reset_index()

unique_tags = list(pd.unique(grp_data.Hashtags))
rndm5_tags=[]
while True:
    tag = random.sample(unique_tags,1)[0]
    x=grp_data[grp_data['Hashtags']==tag]
    
    if len(rndm5_tags)==5:
        break
    if(len(x)<30):
        continue
    elif (tag not in rndm5_tags):
            rndm5_tags.append(tag)
           
print("Hashtags: ",rndm5_tags)

month_wise_count=[]
for tag,k in zip(rndm5_tags,range(1,6)):
    x=grp_entire_data[grp_entire_data['Hashtags']==tag]
    for i in x.Date:
        date=datetime.datetime.strptime(i, "%Y-%m-%d")
        month=cd.month_name[date.month]
        x.loc[x.Date==i,'Date'] = month
    x.rename(columns={'Date':'Month'},inplace=True)
    month_wise_count.append(x)


# In[15]:


#Bar plot of hashtags
month_wise_cnt=[]
for df in month_wise_count:
    df.drop_duplicates(inplace=True)
    month_wise_cnt.append(pd.DataFrame(df.groupby(['Month'],sort=False)['freq'].sum()).reset_index())

months = ['January','February','March','April','May','June','July','August','September','October','November','December']
for i in months:
     for j in range(len(month_wise_cnt)):
            if i not in list(month_wise_cnt[j].Month):
                ind = months.index(i)
                line = pd.DataFrame({"Month": i, "freq": 0}, index=[ind])
                month_wise_cnt[j] = pd.concat([month_wise_cnt[j].iloc[:ind], line, month_wise_cnt[j].iloc[ind:]]).reset_index(drop=True)

for tag,m in zip(rndm5_tags,month_wise_cnt):
    print(tag)
    print(m)
    print('===========')

y_pos = np.arange(len(month_wise_cnt[0].Month))
plt.figure(figsize = (145,45))
plt.subplot(3,3,5)
w = 0.15
plt.bar(y_pos-0.3,month_wise_cnt[0].freq, align='center',color='blue', alpha=0.9,width = w,label=rndm5_tags[0])
plt.bar(y_pos-0.15,month_wise_cnt[1].freq, align='center',color='#f7a013', alpha=0.9,width = w,label=rndm5_tags[1])
plt.bar(y_pos,month_wise_cnt[2].freq, align='center',color='#29d31d', alpha=0.9,width = w,label=rndm5_tags[2])
plt.bar(y_pos+0.15,month_wise_cnt[3].freq, align='center',color='#d80225', alpha=0.9,width = w,label=rndm5_tags[3])
plt.bar(y_pos+0.3,month_wise_cnt[4].freq, align='center',color='yellow', alpha=0.9,width = w,label=rndm5_tags[4])
plt.xticks(y_pos,month_wise_cnt[0].Month,fontsize=25)
plt.xlabel("Month",fontsize=50)
plt.ylabel('Frequency',fontsize=50)
plt.title("Comparison of Hashtags",fontsize=75)
plt.legend(loc=1)
plt.show()

