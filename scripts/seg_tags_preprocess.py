import pandas as pd
from datetime import datetime

twitter = pd.read_csv("../datasets/twitter.csv")
hashtags=pd.read_csv("../datasets/hashtags.csv")
seg_tags=pd.read_csv("../datasets/segmented_tags.csv")

cm_tags = [hashtags,seg_tags]
df_tags = pd.concat(cm_tags,axis=1)

twitter['Hashtags'] = twitter.Hashtags.str.lower()
twitter.drop_duplicates(inplace=True)
twitter.dropna(inplace=True)
twitter.reset_index(drop=True,inplace=True)

date_tags= pd.DataFrame({'freq' : twitter.groupby(['Date','Hashtags']).size()}).sort_values(by=['Date'],ascending=True).reset_index()
for tag,seg_tag in zip(df_tags.Hashtags,df_tags.Seg_Hashtags):
    date_tags.loc[date_tags.Hashtags==tag,'Hashtags'] = seg_tag
date_tags.rename(columns={'Hashtags':'Seg_tags'},inplace=True)

date_tags.reset_index(inplace=True)

grp_date = pd.DataFrame(columns={'keyword','Date','freq'})
grp_date.to_csv('../datasets/words_dates_list_cw.csv',columns={'keyword','Date','freq'},index=False)

# list of dates for a word region wise
for string in seg_tags.Seg_Hashtags:
        x = str(string).split(" ")
        for word in x:
            date_tags['Index'] = list(map(lambda y: word in str(y).split(), date_tags.Seg_tags))
            filtered_date_tags = date_tags[date_tags.Index != False]
            grp_date = pd.DataFrame({'freq' : filtered_date_tags.groupby(['Date']).size()}).sort_values(by=['Date'],ascending=True).reset_index()
            grp_date.insert(0,'keyword',word)
            grp_date.to_csv('words_dates_list.csv',header=False,mode='a',index=False)
            

pp_tags = pd.DataFrame(columns={'keyword','value'})
pp_tags.to_csv('../datasets/words_dates_list_gnrl.csv',columns={'keyword','value'},index=False)

# list of dates for a word in general
for string in seg_tags.Seg_Hashtags:
    x = str(string).split(" ")
    for word in x:
        date_tags['Index'] = list(map(lambda y: word in str(y).split(), date_tags['Seg_tags']))
        Dates = list(set(date_tags.loc[date_tags['Index'] != False].Date))
        rng=(max(pd.to_datetime(Dates))-min(pd.to_datetime(Dates))).days
        values = (Dates,rng)
        pp_tags = pp_tags.append({'keyword' : word , 'value' : values }, ignore_index=True)

pp_tags.to_csv('../datasets/words_dates_list_gnrl.csv',header=False,mode='a',index=False)

