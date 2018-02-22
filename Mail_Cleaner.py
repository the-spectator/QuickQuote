import EFZP as zp
import pandas as pd
import config

def mail_cleaner_main():
	
	print("\nMail Cleaning starting .. ")
	df = pd.read_csv(config.raw_data_csv, encoding='utf-8')
	df['Contents'] = df['Contents'].apply(functionalZone)
#	df['Offer'] = df['Offer'].apply('rem_punct')
#	df['Offer_noise_free'] = apply.('Standardize')	
	df.to_csv(config.raw_data_csv,index=False, encoding = "utf-8")	
	print("Mail cleaning completed ...")

def functionalZone(doc):
	p = zp.parse(doc)
	ans = " "

	if (str(p['body']) is not None):
		ans = ans + str(p['body'])
	if(str(p['reply_text']) is not None):
		ans = ans + str(p['reply_text'])
	return ans

mail_cleaner_main()
