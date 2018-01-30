
# coding: utf-8

# In[1]:

import pandas as pd
import numpy as np


# In[2]:

def process_data(name):
    df = pd.read_csv(name)
    df['Processed'] = df['Contents'].apply(rem_punt)
    df.drop(['Contents'],axis = 1 , inplace = True)
    df['Offer_noise_free'] = df['Offer'].apply(rem_noise)
    df.to_csv('Processed_Data.csv',index=False,encoding = "utf-8")
                                               


# In[3]:

def rem_punt(doc):
    ans = ""
    doc = doc.lower()
    
    index1 = doc.rfind("gender")
    if(index1 == -1):
        index1 = 0
    index2 = doc.rfind("face")
    
    if(index2 == -1):
        ans = doc[index1:]
    else:
        ans = doc[index1:index2]
    return ans        


# In[4]:

lookup = ["tobacco super/standard","super/preferred","non-tobacco/preferred","declined"]

def rem_noise(doc):
    doc = doc.lower()
    for i in lookup:
        if i in doc:
            return i
    return doc


# In[10]:

#import EFZP as zp
#p = zp.parse("Hi Dave,\nLets meet up this Tuesday\nCheers, Tom\n\nOn Sunday, 15 May 2011 at 5:02 PM, Dave Trindall wrote: Hey Tom,\nHow about we get together ...")
#print (p)

