import EFZP as zp
import pandas as pd
import config

def mail_cleaner_main():
	print("\nMail Cleaning starting .. ")
	df = pd.read_csv(config.raw_data_csv, encoding='ISO-8859-1')
	df['Contents'] = df['Contents'].apply(functionalZone)
#	df['Offer'] = df['Offer'].apply()	
	df.to_csv(config.raw_data_csv,index=False, encoding = "utf-8")	
	print("Mail cleaning completed ...")

def functionalZone(doc):
	p = zp.parse(doc)
	return (str(p['body'])+str(p['reply_text']))




