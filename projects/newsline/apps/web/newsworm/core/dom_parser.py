from newsline.apps.utility.logger.core import logger
from newsline.helpers import helpers
from bs4 import BeautifulSoup

import requests

class WormDomParser(logger.ClassUsesLog):

	# Logging info
	log_directory_name = "wormdomparser_logs"
	log_name           = "WormDomParserClass"
	
	@logger.log_method
	def __init__(self, url):
		self.url = ''
		self.dom = ''

		r = None
		if helpers.is_url(url):
			if helpers.has_http_prefix(url):
				self.url = url
			else:
				self.url = "http://" + url
		else:
			raise ValueError("Url not valid.")

		self.log("Provided url: %s | Valid" % self.url)
		headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

		self.log("[GET][%s] ..." % self.url)
		r = requests.get(self.url, headers=headers)
		# except requests.exceptions.ConnectionError as e:

		if r is not None:
			if r.status_code == 200 :
				# self.log("[GET][SUCCESS][200]", color="GREEN")
				self.dom = BeautifulSoup(r.text, 'html.parser')
			else:
				self.log("[GET][FAILURE][%s]" % r.status_code, color="RED")
		else:
			raise ValueError("the url can not be None")

	@logger.log_method
	def find(self, css_selector_path):
		self.log("Looking for dom path: %s" % css_selector_path)
		return self.dom.select(css_selector_path)


