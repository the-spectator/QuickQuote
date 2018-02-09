# coding: utf-8

# File imports

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


df = pd.read_csv("Data/PProcessed.csv", encoding='UTF-8')
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

df.to_csv('Data/NLPProcessed.csv',index=False, encoding = "utf-8")

df = pd.read_csv('Data/NLPProcessed.csv')


# Statistical Modeling 

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.decomposition import TruncatedSVD
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import Normalizer,LabelEncoder
from sklearn.metrics import accuracy_score,classification_report


X = df['Lemmitize']
of = pd.read_csv('Data/raw_data1.csv', encoding='ISO-8859-1')
y = of['Offer']

X[0]

X_train,X_test,y_train,y_test = train_test_split(X,y)

vect = TfidfVectorizer(max_df=0.8, max_features=15000, min_df=0.01, use_idf=True , ngram_range=(1,3))

#from xgboost.sklearn import XGBClassifier
#model1 = XGBClassifier(nthread=4,n_estimators=1000)


# Naive Bayes

from sklearn.naive_bayes import GaussianNB,MultinomialNB
model2 = GaussianNB()


# ExtraTree Classifier

from sklearn.ensemble import ExtraTreesClassifier,RandomForestClassifier
model3 = RandomForestClassifier(n_estimators=60,n_jobs=3,max_features = "auto", min_samples_leaf = 50)

# SVM Classifier

from sklearn.svm import SVC
model4 = SVC(kernel='rbf', C=100,gamma=10)


# Logistic Regression 

from sklearn.linear_model import LinearRegression,SGDClassifier,LogisticRegression
model5 = LogisticRegression()

from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
model6 = LinearDiscriminantAnalysis()

from sklearn import linear_model
model7 = linear_model.SGDClassifier()

import pickle

def model_saving(model_name,model):
    filename = model_name +'.sav'
    pickle.dump(model, open('SavedModels/'+filename, 'wb'))
    
# Model Fitting

import matplotlib.pyplot as plt
from sklearn.metrics import classification_report
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
import time

name = [] 
results = []
matrix_confusion = []
training_time = []
prediction_time = []

def model_making(model_name, vect , model , X_train , y_train , X_test , y_test):
    
    t1 =time.time()
    clf = make_pipeline(vect,model)
    clf.fit(X_train,y_train)
    t2 = time.time()
    training_time.append(t2-t1)
    model_saving(model_name,clf)
    t1 = time.time()
    pd = clf.predict(X_test)
    t2 = time.time()
    prediction_time.append(t2-t1)
    
    y_pred = clf.predict(X_test)
    name.append(model_name)
    results.append(accuracy_score(y_test, y_pred)*100)
    matrix_confusion.append(confusion_matrix(y_test, y_pred))

model_making("Random Forest",vect, model3, X_train, y_train, X_test, y_test)

model_making("SVM" , vect, model4, X_train, y_train, X_test, y_test)

model_making("Logistic Regression",vect, model5, X_train, y_train, X_test, y_test)

model_making("SGDClassifier",vect, model7, X_train, y_train, X_test, y_test)

print("Total dataset",len(X))
print("Training dataset: ",len(X_train))
print("Testing dataset: ",len(X_test),"\n")
print("{:20} {:^20} {:^20} {:^20}\n ".format("Name" , "Accuracy" , "Training Time(s)" , "Prediction Time(s)" ) )

for i in range(len(name)):
    print("{:20} {:^20.3f} {:^20.3f} {:20.3f}s \n ".format(name[i] , results[i] , training_time[i] , prediction_time[i] ) )


print(X_test)


loaded_model = pickle.load(open('SavedModels/SVM.sav', 'rb'))
result = loaded_model.score(X_test, y_test)
print(result)

'''

parameters = {'kernel':('linear', 'rbf'), 'C':[1, 10]}

from sklearn.model_selection import GridSearchCV
gridS = GridSearchCV(model4, parameters)
gridS.fit(X_train,y_train)
y_pred = gridS.predict(X_test)
print("=====Accuracy Score ", "{0:.2f}".format(accuracy_score(y_test, y_pred)*100), "%")

'''
