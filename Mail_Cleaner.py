import EFZP as zp
import pandas as pd
import config
import logging

logging.basicConfig(filename="Data/logfile.log", level=logging.DEBUG)


def mail_cleaner_main(file):
	
	logging.debug("\nMail Cleaning starting .. ")
	# print(config.raw_data_csv)
	df = pd.read_csv(file, encoding='utf-8')
	df['Contents'] = df['Contents'].apply(functionalZone)
#	df['Offer'] = df['Offer'].apply('rem_punct')
#	df['Offer_noise_free'] = apply.('Standardize')	
	df.to_csv(file,index=False, encoding = "utf-8")	
	logging.debug("Mail cleaning completed ...")

def functionalZone(doc):
	p = zp.parse(doc)
	ans = " "

	if (str(p['body']) is not None):
		ans = ans + str(p['body'])
	if(str(p['reply_text']) is not None):
		ans = ans + str(p['reply_text'])
	return ans

# mail_cleaner_main(config.eraw_data_csv)
