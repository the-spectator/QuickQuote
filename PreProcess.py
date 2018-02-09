# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import re
import config

df = pd.read_csv(config.regex_processed_csv, encoding='UTF-8')
df = df.iloc[1:]
df = df.drop(columns=['Year_of_birth'])



def changeFace(ans):
    
    val = re.sub("Face Amount: ",' ',ans)
    
    val = re.sub(",",' ',val)
    val = str(re.sub(" ",'',val))
    index = (val.find('$'))
    if(index!=-1):
        val = val[1:]
        
    #val = int(val)
    return (val)


df['Face Amount'] = df['Face Amount'].apply(changeFace)

def changeWt(ans):
    
    val = re.sub("#",'lb',ans)
    
    val = re.sub("lbs",'lb',val)
    val = str(re.sub(" ",'',val))
    if(re.search('KG|Kg|kg',val, re.I | re.U)):
        x = re.findall(r'\d+',ans)
        val = str(int(int(x[0])*2.2)) + 'lb'
    #val = int(val)
    return (val)


df['Weight'] = df['Weight'].apply(changeWt)

df.to_csv(config.preprocessed_csv,index=False, encoding = "utf-8")
