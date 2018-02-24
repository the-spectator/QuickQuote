# -*- coding: utf-8 -*-

from RegexProcessing import regex_processing_main
from PreProcess import preprocess_main
from Model_Training import model_making_main
from Mail_Cleaner import mail_cleaner_main
import config
import logging

logging.basicConfig(filename="Data/logfile.log", level=logging.DEBUG)

def model_maker_main():

	# config.raw_data_csv = 'Data/raw_data1.csv'
	mail_cleaner_main(config.raw_data_csv)
	regex_processing_main(config.raw_data_csv)
	preprocess_main(config.raw_data_csv)
	model_making_main(config.raw_data_csv)
	logging.debug("Completed ...")

model_maker_main()
