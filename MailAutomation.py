from imapclient import IMAPClient
from secrets import EMAIL, PASSWORD
from config import imap_server, imap_port
import email
import lxml.html
import csv, os.path

def clean(data):
	#employing the lxml parser to clean the content of mail
	#every other thing is pretty self explanatory
	doc  = lxml.html.document_fromstring(data)
	newdata = doc.text_content().encode('utf8').decode('utf8').strip()
	if (newdata[:42] == '<!-- P {margin-top:0;margin-bottom:0;} -->'):
		newdata = newdata[44:]
	return newdata.strip()

def get_decoded_email_body(message_body):
    """ Decode email body.
    Detect character set if the header is not set.
    We try to get text/plain, but if there is not one then fallback to text/html.
    :param message_body: Raw 7-bit message body input e.g. from imaplib. Double encoded in quoted-printable and latin-1
    :return: Message body as unicode string
    """
    msg = email.message_from_string(message_body)

    text = ""
    if msg.is_multipart():
        html = None
        for part in msg.get_payload():
            #print( "%s, %s" % (part.get_content_type(), part.get_content_charset()))
            if part.get_content_charset() is None:
                # We cannot know the character set, so return decoded "something"
                text = part.get_payload(decode=True)
                continue

            charset = part.get_content_charset()

            if part.get_content_type() == 'text/plain':
                text = str(part.get_payload(decode=True), str(charset), "ignore").encode('utf8', 'replace')

            if part.get_content_type() == 'text/html':
                html = str(part.get_payload(decode=True), str(charset), "ignore").encode('utf8', 'replace')

        if text is not None:
            return text.strip()
        else:
        	return html.strip()
    else:
    	text = str(msg.get_payload(decode=True), msg.get_content_charset(), 'ignore').encode('utf8', 'replace')
    	return text.strip()

def write_to_csv(filename, data_dict):
	file_exists = os.path.isfile(filename)
	# Writing it into csv file
	with open(filename, 'a', encoding = 'utf8') as csvfile:
	    fieldnames = ['id', 'message_id', 'subject', 'Sender/email', 'recpient mail', 'sendOn', 'receivedOn', 'Offer', 'Contents']
	    writer = csv.DictWriter(csvfile, fieldnames=fieldnames) 
	    if not file_exists:
	    	writer.writeheader()
	    writer.writerows(data_dict)
		

def mail_reader(folder,flags):
	server = IMAPClient(imap_server, imap_port, use_uid = True, ssl = True)
	server.login(EMAIL, PASSWORD)

	# Selecting the inbox folder
	message_box = server.select_folder(folder)
	
	# Gives list of unread messages
	messages = server.search(flags)
	# print(messages)
	
	# get_flags method gives the flags(Unseen or Seen) for each message 
	# print(server.get_flags(messages))

	# Get the id, msg_id, subject, date, sender_email, receiver_email, content from email
	body = server.fetch(messages, ['ENVELOPE','RFC822'])
	data_dict = []
	for msgid,data in body.items():
		envelope = data[b'ENVELOPE']
		content_raw = data[b'RFC822'].decode('utf8')
		content = clean(get_decoded_email_body(content_raw).decode('utf8'))
		date = envelope.date
		message_id = envelope.message_id.decode('utf8')
		subject = envelope.subject.decode('utf8')
		from_ = str(envelope.from_[0])
		to = str(envelope.to[0])
		row = {'id': msgid, 'message_id': message_id, 'subject': subject, 'Sender/email': from_, 'recpient mail': to, 'sendOn': date, 'receivedOn': date, 'Offer': None, 'Contents': content}
		data_dict.append(row)

	# Writing data to csv
	write_to_csv('raw_data.csv', data_dict)

	# to set messages unseen to mark it seen use [b'\\Seen']
	server.set_flags(messages,[])
	
	# messages = server.search(['ALL'])
	# print(server.get_flags(messages))
	server.logout()

# For getting all unread emails from inbox
mail_reader('INBOX',['SEEN'])

# For getting all emails from sentbox
# mail_automation('SENT',['ALL'])

