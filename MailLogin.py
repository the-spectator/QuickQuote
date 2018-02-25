# -*- coding: utf-8 -*-

from imapclient import IMAPClient
from secrets import EMAIL, PASSWORD
import logging
import config

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def login():
	logger.debug('Establishing Connections ....')
	server = IMAPClient(config.imap_server, use_uid = True, ssl = True)
	server.login(EMAIL, PASSWORD)
	logger.debug('Connection Established ....')
	return server