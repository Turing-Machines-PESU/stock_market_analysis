
# coding: utf-8

# In[1]:


import pandas as pd
from datetime import datetime


# In[11]:


twitter = pd.read_csv("twitter.csv")
hashtags=pd.read_csv("hashtags.csv")
seg_tags=pd.read_csv("segmented_tags.csv")


# In[12]:


cm_tags = [hashtags,seg_tags]
df_tags = pd.concat(cm_tags,axis=1)


# In[13]:


twitter['Hashtags'] = twitter.Hashtags.str.lower()
twitter.drop_duplicates(inplace=True)
twitter.dropna(inplace=True)
twitter.reset_index(drop=True,inplace=True)


# In[20]:


date_tags= pd.DataFrame({'freq' : twitter.groupby(['Date','Hashtags']).size()}).sort_values(by=['Date'],ascending=True).reset_index()
for tag,seg_tag in zip(df_tags.Hashtags,df_tags.Seg_Hashtags):
    date_tags.loc[date_tags.Hashtags==tag,'Hashtags'] = seg_tag
date_tags.rename(columns={'Hashtags':'Seg_tags'},inplace=True)


# In[21]:


date_tags.reset_index(inplace=True)


# In[22]:


grp_date = pd.DataFrame(columns={'keyword','Date','freq'})
grp_date.to_csv('words_dates_list_cw.csv',columns={'keyword','Date','freq'},index=False)


# In[23]:


# list of dates for a word
for string in seg_tags.Seg_Hashtags:
        x = str(string).split(" ")
        for word in x:
            date_tags['Index'] = list(map(lambda y: word in str(y).split(), date_tags.Seg_tags))
            filtered_date_tags = date_tags[date_tags.Index != False]
            grp_date = pd.DataFrame({'freq' : filtered_date_tags.groupby(['Date']).size()}).sort_values(by=['Date'],ascending=True).reset_index()
            grp_date.insert(0,'keyword',word)
            grp_date.to_csv('words_dates_list_cw.csv',header=False,mode='a',index=False)
            


# In[160]:


pp_tags = pd.DataFrame(columns={'keyword','value'})
pp_tags.to_csv('words_dates_list_gnrl.csv',columns={'keyword','value'},index=False)


# In[161]:


# list of dates for a word in general
for string in seg_tags.Seg_Hashtags:
    x = str(string).split(" ")
    for word in x:
        date_tags['Index'] = list(map(lambda y: word in str(y).split(), date_tags['Seg_tags']))
        Dates = list(set(date_tags.loc[date_tags['Index'] != False].Date))
        rng=(max(pd.to_datetime(Dates))-min(pd.to_datetime(Dates))).days
        values = (Dates,rng)
        pp_tags = pp_tags.append({'keyword' : word , 'value' : values }, ignore_index=True)


# In[ ]:


pp_tags.to_csv('words_dates_list_gnrl.csv',header=False,mode='a',index=False)

