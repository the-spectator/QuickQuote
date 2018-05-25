# -*- coding: utf-8 -*-

from imapclient import IMAPClient
from secrets import EMAIL, PASSWORD
from email.message import EmailMessage
from email.headerregistry import Address
from MailLogin import login
import email.utils
import pandas as pd
import config
import collections
import os
import logging

logger = logging.getLogger('QQ')


def give_email_address(addresses):
	parts = email.utils.getaddresses(addresses)
	username, domain = parts[0][1].split('@')
	display_name = parts[0][0]
	address = Address(display_name=display_name,
					  username=username, domain=domain)
	return address

# Create the base text message.


def create_email(email_to, email_subject, email_from, email_content):
	msg = EmailMessage()
	msg['Subject'] = email_subject
	msg['From'] = email_from
	msg['To'] = email_to
	msg.set_content(email_content)
	return bytes(msg)


# Reading Template from email.template
def read_template():
	with open(config.template, 'r', encoding='utf8') as file:
		email_template = file.read()
	return email_template


# Marking the predicted emails

def mark_predicted(id, message_id):
	entry = collections.OrderedDict({'ID': id, 'MessageID': message_id})
	df = pd.DataFrame([entry])
	file_exists = os.path.isfile(config.predicted_csv)
	if not file_exists or os.stat(config.predicted_csv).st_size == 0:
		df.to_csv(config.predicted_csv, header=True,
				  index=False, encoding='utf-8')
	else:
		df.to_csv(config.predicted_csv, mode='a', index=False,
				  header=False, encoding='utf-8')


def append_mail(doc, server, folder, new_flags):
	email_to = give_email_address([doc['Senderemail']])
	email_from = give_email_address([config.email_from])
	email_subject = f"Re:{doc['Subject']}"
	result = doc['Offer_noise_free']
	print(result)
	result = result.split("'")[1::2][0]
	email_template = read_template()
	disclaimer = get_disclaimer(result)
	email_content = email_template.format(product_=result, from_=doc['Senderemail'], 
										  subject_=doc['Subject'], sendon_=doc['SentOn'],
										  content_=doc['Contents'], disclaimer_= disclaimer)
	mail = create_email(email_to, email_subject, email_from, email_content)
	server.append(folder, mail, flags=(new_flags), msg_time=None)
	mark_predicted(doc['ID'], doc['MessageID'])
	pass

def get_disclaimer(result):
	condition1 = 'Applicable only with medical certificate provided.'
	condition2 = 'Periodic medical examination is advised.'
	condition4 = 'These quotes are not final and are purely based on information provided by customer.'
	condition3 = 'Further financial analysis is needed.'
	disclaimer = ''
	if result == 'Preferred Non-Tobacco':
		disclaimer+='1. ' + condition1
		disclaimer+='\n2. ' + condition3
	elif result == 'Preferred':
		disclaimer+='\n1. ' + condition1
		disclaimer+='\n2. ' + condition2
		disclaimer+='\n3. ' + condition4
	else:
		disclaimer+='\n1. ' + condition1
		disclaimer+='\n2. ' + condition2
		disclaimer+='\n3. ' + condition3
		disclaimer+='\n4. ' + condition4
	return disclaimer

def mail_append_main():
	logger.info('>> Start - Mail Append')
	server = login()
	df = pd.read_csv(config.eraw_data_csv, encoding='utf8')
	df.apply(append_mail, args=(server, config.append_box, []), axis=1)
	server.logout()
	logger.info('<< End - Mail Append')

# mail_append_main()
