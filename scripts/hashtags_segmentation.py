import pandas as pd
from wordsegment import load,segment
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize,RegexpTokenizer 
import re

# hashtag segmentation 
def seg(text):
    if isinstance(text,str):
        if " " in text:
            return text
        else:
            pattern=re.compile("[^\w']")
            a = pattern.sub('', text)
            #print(a)
            load() 
            segmentedText=segment(a)
            completeText = ' '.join([e for e in segmentedText])

        return completeText

    else:
        raise Exception("Value must be of the type str")

# filtering tags
def remove_stop_words(text):
    if isinstance(text,str):
        stop_words = set(stopwords.words('english'))
        tokenizer = RegexpTokenizer(r'\w+') 
        word_tokens = tokenizer.tokenize(text) 
        filtered_sentence = ' '.join([w for w in word_tokens if not w in stop_words and w.isalnum()])
        return filtered_sentence
    else:
        raise Exception("Value must be of the type str")

hashtags=pd.read_csv("../datasets/hashtags.csv")

pp_tags = pd.DataFrame(columns={'Hashtags'})
for tag in hashtags.Hashtags:
    x=seg(tag)
    text=(remove_stop_words(x))
    pp_tags = pp_tags.append({'Hashtags': text}, ignore_index=True)

pp_tags.to_csv('../datasets/segmented_tags.csv',index=False,sep='\t')

