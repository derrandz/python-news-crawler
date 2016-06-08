from newsline.functionalities.tests.base_simple_test import BaseSimpleTestCase
from newsline.helpers.colors_class import ColorsClass

from lxml import html

from newsline.apps.web.newsworm.core.dom_parser import StaticDomParser
class DomParserTestCase(BaseSimpleTestCase):
	''' A test suit for divergence decorators. '''

	def testEncodingForWebsite(website, selector):
		import requests
		from bs4 import BeautifulSoup as BS

		# this website has as an encoding: Windows1256 that is ISO-8859-1
		ws = requests.get(website)
		if ws.status_code != 200:
			print("Failed to make the requets")
			return

		print("[GET][SUCCESS][%s]" % website)
		print("[%s][ENCODING]" % ws.encoding)

		text = ws.text.encode(ws.encoding)

		ws = BS(text, 'html.parser')
		import urllib.parse

		ws = [a.get("href")for a in ws.select(selector)]
		print("\n\nBefore unquote")
		for a in ws:
			print("%s ." % a)


		ws = [urllib.parse.unquote(a) for a in ws]
		print("\n\nAfter unquote")
		for a in ws:
			print("%s ." % a)

	def testEncoding(self):
		testEnc = self.__class__.testEncodingForWebsite
		testEnc("http://chaabpress.com", "div.navbarr > ul > li > a")
		testEnc("http://kifache.com", "ul.nav > li.menu-item > a")