# -*- coding: utf-8 -*-

from RegexProcessing import regex_processing_main
from PreProcess import preprocess_main
from MailAutomation import mail_reader
from Prediction import prediction_main
from mail_append import mail_append_main

def prediction_maker_main():
	mail_reader('INBOX', ['UNSEEN'], [])
	regex_processing_main()
	preprocess_main()
	prediction_main()
	mail_append_main()
	print("Completed ...")

prediction_maker_main()
