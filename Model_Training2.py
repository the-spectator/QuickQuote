import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import config


df = pd.read_csv(config.preprocessed_csv, encoding='UTF-8')
df['ColumnA'] = df[df.columns[0:11]].apply(lambda x: ','.join(x.dropna()),axis=1)
#print(df['ColumnA'][1])

from nltk.corpus import stopwords,wordnet as wn
from nltk.tokenize import wordpunct_tokenize,sent_tokenize
from nltk import pos_tag
from nltk.stem.wordnet import WordNetLemmatizer
import re

#Removes all punctuations which acts as noise

def rem_punt(doc):
    ans = re.sub('"|\\n|\(|\)|\.|[$!--+@#:]',' ',doc)
    ans = re.sub(' +',' ',ans)
    ans = ans.lower()
    return ans


# Stop words removal using tokenization

stop_word = set(stopwords.words('english'))

def tokenize(document): 
    lemmy = []
    for sent in sent_tokenize(document):
        for token, tag in pos_tag(wordpunct_tokenize(sent)):
            #print(token,tag)
            if token in stop_word:
                 continue
            lemma = lemmatize(token, tag)
            lemmy.append(lemma)
    return lemmy

#Lemmatization for tokens simplification

def lemmatize(token, tag):
    tag = {
          'N': wn.NOUN,
          'V': wn.VERB,
          'R': wn.ADV,
          'J': wn.ADJ
    }.get(tag[0], wn.NOUN)
    lemmatizer = WordNetLemmatizer()
    return lemmatizer.lemmatize(token, tag)


# In[22]:


# In[22]:

df['Lemmitize'] = df['ColumnA'].apply(rem_punt).apply(tokenize)

df.to_csv(config.nlp_processed_csv,index=False, encoding = "utf-8")

df = pd.read_csv(config.nlp_processed_csv)


# Statistical Modeling 

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.decomposition import TruncatedSVD
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import Normalizer,LabelEncoder
from sklearn.metrics import accuracy_score,classification_report


X = df['Lemmitize']
of = pd.read_csv(config.raw_data_csv, encoding='ISO-8859-1')
y = of['Offer']

X[0]

print("original")
print(y.values)

X_train,X_test,y_train,y_test = train_test_split(X,y)

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import BernoulliNB

from sklearn.pipeline import Pipeline

pipeline = Pipeline([
    ('vectorizer',  CountVectorizer(ngram_range=(1, 2))),
    ('tfidf_transformer',  TfidfTransformer()),
    ('classifier',  BernoulliNB(binarize=0.0)) ])

pipeline.fit(X_train.values, y_train.values)
print(pipeline.predict(X_test))
print(y_test.values)


print(pipeline.get_params()['vectorizer'])






