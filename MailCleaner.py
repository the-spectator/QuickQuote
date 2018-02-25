import EFZP as zp
import pandas as pd
import config
import logging

logging.basicConfig(filename=config.log_file, level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def mail_cleaner_main(file):
	
	logger.debug("Mail Cleaning starting .. ")
	df = pd.read_csv(file, encoding='utf-8')
	df['Contents'] = df['Contents'].apply(functionalZone)
	# df['Offer'] = df['Offer'].apply('rem_punct')
	# df['Offer_noise_free'] = apply.('Standardize')	
	df.to_csv(file,index=False, encoding = "utf-8")	
	logger.debug("Mail cleaning completed ...")

def functionalZone(doc):
	p = zp.parse(doc)
	ans = " "

	if (str(p['body']) is not None):
		ans = ans + str(p['body'])
	if(str(p['reply_text']) is not None):
		ans = ans + str(p['reply_text'])
	return ans

# mail_cleaner_main(config.eraw_data_csv)
