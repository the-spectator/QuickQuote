# -*- coding: utf-8 -*-


from MailAutomation import mail_reader
from Prediction import prediction_main
from MailAppend import mail_append_main
import config
import os
import logging

logger = logging.getLogger('QQ')


def prediction_maker_main():
	logger.info(">> Start - Predection maker")

	mail_reader(config.email_box, config.email_flags, config.email_new_flags)
	if os.stat(config.eraw_data_csv).st_size <= 1:
		logging.warn("No UnRead/UnPredicted mails found.")
		return

	prediction_main(config.eraw_data_csv)
	mail_append_main()
	logger.info("<< End - Predection maker")

prediction_maker_main()
