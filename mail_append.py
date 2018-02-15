from imapclient import IMAPClient
from secrets import EMAIL, PASSWORD
from email.message import EmailMessage
from email.headerregistry import Address
import email.utils
import pandas as pd
import config

def split_combined_addresses(addresses):
    parts = email.utils.getaddresses(addresses)
    print(parts)
    return [email.utils.formataddr(name_addr) for name_addr in parts]

def read_file():
	df = pd.read_csv(config.eraw_data_csv, encoding='UTF-8')
	parts = email.utils.getaddresses([df['recpient mail'][2]])
	print(parts)
	print([email.utils.formataddr(name_addr) for name_addr in parts])
	#print(split_combined_addresses(df['recpient mail'][2]))
	pass

# Create the base text message.
def create_email():
	msg = EmailMessage()
	msg['Subject'] = "Ayons asperges pour le déjeuner"
	msg['From'] = Address("Pepé Le Pew", "pepe", "example.com")
	msg['To'] = (Address("Penelope Pussycat", "penelope", "example.com"),)
	msg.set_content("""\
	Salut!

	Cela ressemble à un excellent recipie[1] déjeuner.

	[1] http://www.yummly.com/recipe/Roasted-Asparagus-Epicurious-203718

	--Pepé
	""")
	return bytes(msg)


def main():
	folder = 'Test'
	server = IMAPClient(config.imap_server, config.imap_port, use_uid = True, ssl = True)
	server.login(config.EMAIL, config.PASSWORD)

	server.append(folder, create_email(), flags=([]), msg_time = None)

read_file()