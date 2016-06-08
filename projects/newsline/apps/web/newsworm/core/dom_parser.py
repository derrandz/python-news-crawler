from newsline.apps.utility.logger.core import logger
from newsline.helpers import helpers

from bs4 import BeautifulSoup
import requests

class StaticDomParser(logger.ClassUsesLog):

	"""
		A regular dom parser that returns html content post an HTTP request.
	"""
	# Logging info
	log_directory_name = "wormdomparser_logs"
	log_name           = "WormDomParserClass"
	
	def __init__(self, url):
		self.url = ''
		self.dom = ''

		if helpers.is_url(url):
			if helpers.has_http_prefix(url):
				self.url = url
			else:
				self.url = "http://" + url
		else:
			raise ValueError("Url not valid.")

		self.log("Provided url: %s | Valid" % self.url)
		self.log("[GET][%s] ..." % self.url)


		self.log("[SLEEP: 7s]")

		from time import sleep
		sleep(7) # delays for 5 seconds

		try:
			headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
			r = requests.get(self.url, headers=headers)
		except requests.exceptions.ConnectionError as e:
			self.dom = BeautifulSoup('<html><div>"Connection refused"</div><div>%s</div></html>' % str(e), 'html.parser')
		else:
			if r.status_code == 200 :
				self.log("[GET][SUCCESS][200]", color="GREEN")
				self.dom = BeautifulSoup(r.text, 'html.parser')
			else:
				self.log("[GET][FAILURE][%s]" % r.status_code, color="RED")
				self.dom = BeautifulSoup('<html>%s</html>' % r.status_code, 'html.parser')


	def find(self, css_selector_path):
		self.log("Looking for dom path: %s" % css_selector_path)
		return self.dom.select(css_selector_path)