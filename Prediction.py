# coding: utf-8

# File imports

import pandas as pd
import numpy as np
import config
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
def tokenize(document): 
    lemmy = []
    stop_word = set(stopwords.words('english'))
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

import pickle
def PredictionModule(doc):
	loaded_model = pickle.load(open('SavedModels/SVM.sav', 'rb'))
	
	pd = loaded_model.predict([doc])
	print(pd)


def main():

	df = pd.read_csv(config.eraw_data_csv, encoding='ISO-8859-1')
	df['ColumnA'] = df[df.columns[0:10]].apply(lambda x: ','.join(x.dropna()),axis=1)

	df['Lemmitize'] = df['ColumnA'].apply(rem_punt).apply(tokenize)
	df.to_csv(config.enlp_processed_csv,index=False, encoding = "utf-8")
	df = pd.read_csv(config.enlp_processed_csv)		#change when merged with email raw data
	df['Lemmitize'].apply(PredictionModule)

main()
	



