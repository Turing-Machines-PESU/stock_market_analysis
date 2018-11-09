import pandas as pd
from datetime import datetime

twitter = pd.read_csv("../datasets/twitter.csv")
hashtags=pd.read_csv("../datasets/hashtags.csv")
seg_tags=pd.read_csv("../datasets/segmented_tags.csv")

twitter['Hashtags'] = twitter.Hashtags.str.lower()
twitter.drop_duplicates(inplace=True)
twitter.dropna(inplace=True)
twitter.reset_index(drop=True,inplace=True)

date_tags= pd.DataFrame({'freq' : twitter.groupby(['Date','Hashtags']).size()}).sort_values(by=['Date'],ascending=True).reset_index()

pp_tags = pd.DataFrame(columns={'keyword','value'})
pp_tags.to_csv('../datasets/words_dates_list.csv',columns={'keyword','value'},index=False)

# list of dates for a word
for string in seg_tags.Hashtags:
    try:
        x = string.split(" ")
        for word in x:
            date_tags['Index'] = list(map(lambda y: y.find(word), date_tags['Hashtags']))
            Dates = list(set(date_tags.loc[date_tags['Index'] != -1].Date))
            rng=(max(pd.to_datetime(Dates))-min(pd.to_datetime(Dates))).days
            values = (Dates,rng)
            pp_tags = pp_tags.append({'keyword' : word , 'value' : values }, ignore_index=True)
    except:
        pass

pp_tags.to_csv('../datasets/words_dates_list.csv',header=False,mode='a',index=False)

