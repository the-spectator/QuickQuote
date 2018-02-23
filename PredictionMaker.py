# -*- coding: utf-8 -*-


from MailAutomation import mail_reader
from Prediction import prediction_main
from mail_append import mail_append_main
import config
import os

def prediction_maker_main():
	mail_reader(config.email_box, config.email_flags, config.email_new_flags)
	if os.stat(config.eraw_data_csv).st_size <= 1 :
    		print('>> Nothing to Predict....')
    		return
	prediction_main(config.eraw_data_csv)
	mail_append_main()
	print("Completed ...")

prediction_maker_main()
