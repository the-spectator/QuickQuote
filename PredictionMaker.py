# -*- coding: utf-8 -*-


from MailAutomation import mail_reader
from Prediction import prediction_main
from mail_append import mail_append_main
import config
def prediction_maker_main():
	print('Fetching Mails ...')
	mail_reader('INBOX', ['UNSEEN'], [])
	print('Mail Downloaded')
	config.raw_data_csv = 'Data/eraw_data.csv'
	prediction_main()
	print("Completed ...")

prediction_maker_main()
