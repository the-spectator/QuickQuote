# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import re
import config
import logging

logging.basicConfig(filename="Data/logfile.log", level=logging.DEBUG)

def changeFace(ans):
    
    val = re.sub("Face Amount: ",' ',ans)
    
    val = re.sub(",",' ',val)
    val = str(re.sub(" ",'',val))
    index = (val.find('$'))
    if(index!=-1):
        val = val[1:]
        
    #val = int(val)
    return (val)



def changeWt(ans):
    
    val = re.sub("#",'lb',ans)
    
    val = re.sub("lbs",'lb',val)
    val = str(re.sub(" ",'',val))
    if(re.search('KG|Kg|kg',val, re.I | re.U)):
        x = re.findall(r'\d+',ans)
        val = str(int(int(x[0])*2.2)) + 'lb'
    #val = int(val)
    return (val)
def emailfirst(doc):
	if(type(doc)==str):
		mails = doc.split(";")
		return str(mails[0])
	else:
		doc = ""
		return doc
def preprocess_main(file):
	logging.debug("Pre processing starting .. ")
	df = pd.read_csv(config.regex_processed_csv, encoding='UTF-8')
	df = df.iloc[1:]
	df = df.drop(columns=['Year_of_birth'])
	
	of = pd.read_csv(file,encoding = 'UTF-8')
	
	of['Senderemail'] = of['Senderemail'].apply(emailfirst)
	df['Senderemail'] = of['Senderemail'].values
	df['Weight'] = df['Weight'].apply(changeWt)
	logging.debug("Weight updation completed.. ")
	df['Face Amount'] = df['Face Amount'].apply(changeFace)
	logging.debug("Face amount updation completed ... ")

	df.to_csv(config.preprocessed_csv,index=False, encoding = "utf-8")
	logging.debug("Pre processing completed ...")
	
# preprocess_main(config.raw_data_csv)
