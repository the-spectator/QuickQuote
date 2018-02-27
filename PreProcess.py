# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import re
import config
import logging

logger = logging.getLogger('QQ')


def changeFace(ans):
	ans = str(ans)
	val = re.sub("Face Amount: ", ' ', ans)
	val = re.sub(",", ' ', val)
	val = str(re.sub(" ", '', val))
	index = (val.find('$'))
	if(index != -1):
		val = val[1:]

	#val = int(val)
	return (val)


def changeWt(ans):
	ans = str(ans)
	val = re.sub("#", 'lb', ans)
	val = re.sub("lbs", 'lb', val)
	val = str(re.sub(" ", '', val))
	if(re.search('KG|Kg|kg', val, re.I | re.U)):
		x = re.findall(r'\d+', ans)
		val = str(int(int(x[0]) * 2.2)) + 'lb'
	#val = int(val)
	return (val)


def emailfirst(doc):
	if(type(doc) == str):
		mails = doc.split(";")
		return str(mails[0])
	else:
		doc = ""
		return doc


def preprocess_main(file):
	logger.info(">> Start - Preprocessing. Standardize Face amount, Weight... etc")
	logger.debug("Opening -" + config.regex_processed_csv)
	df = pd.read_csv(config.regex_processed_csv, encoding='UTF-8')
	# df = df.iloc[1:]
	df = df.drop(columns=['Year_of_Birth'])
	of = pd.read_csv(file, encoding='UTF-8')
	of['recepientemail'] = of['recepientemail'].apply(emailfirst)
	df['recepientemail'] = of['recepientemail'].values

	logger.info("Standardize Weight")
	df['Weight'] = df['Weight'].apply(changeWt)

	logger.info("Standardize Face amount")
	df['Face Amount'] = df['Face Amount'].apply(changeFace)

	df.to_csv(config.preprocessed_csv, index=False, encoding="utf-8")
	logger.info("<< End - Preprocess")

# preprocess_main(config.raw_data_csv)
