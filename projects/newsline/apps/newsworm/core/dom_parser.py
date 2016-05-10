from . import helpers
from bs4 import BeautifulSoup

import requests

class WormDomParser:

	def __init__(self, url):
		self.url = ''
		self.dom = ''

		r = None
		if helpers.is_url(url):
			if helpers.has_http_prefix(url):
				self.url = url
				r = requests.get(url)
			else:
				self.url = "http://" + url
				r = requests.get("http://"+url)
		else:
			raise ValueError("Url not valid.")


		if r is not None:
			if r.status_code == 200 :
				self.dom = BeautifulSoup(r.text, 'html.parser')
			else:
				raise ValueError("Could not perform request : %s | %d"% (r.text, r.status_code))
		else:
			raise ValueError("the url can not be None")

	def find(self, css_selector_path):
		return self.dom.select(css_selector_path)


