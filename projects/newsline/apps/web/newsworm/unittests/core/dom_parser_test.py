from newsline.functionalities.tests.base_simple_test import BaseSimpleTestCase
from newsline.helpers.colors_class import ColorsClass

from lxml import html

from newsline.apps.web.newsworm.core.dom_parser import DynamicDomParser, StaticDomParser
class DomParserTestCase(BaseSimpleTestCase):
	''' A test suit for divergence decorators. '''
	def dynamicParserTest(self):

		url = 'http://pycoders.com/archive/'  
		r = DynamicDomParser.Render(url)  

		#Now using correct Xpath we are fetching URL of archives
		archive_links = [a.get("href") for a in r.find('div.campaign > a')] 
		print(archive_links)

	def testDifference(self):
		r = [a.get('href') for a in StaticDomParser('http://www.alyaoum24.com/news/policy').find('h3 > a')]

		self.print_info("Static crawl, results: %d link" % len(r))
		for a in r:
			self.print_info("%s " % a)

		self.print_seperator()

		r = [a.get('href') for a in DynamicDomParser.Render('http://www.alyaoum24.com/news/policy').find('h3 > a')]

		self.print_info("Dynamic crawl, results: %d link" % len(r))
		for a in r:
			self.print_info("%s " % a)

	def testISOEncoding(self):
		import requests
		from bs4 import BeautifulSoup as BS

		# this website has as an encoding: Windows1256 that is ISO-8859-1
		chaab = requests.get("http://chaabpress.com")
		chaab.text.encoding = 'utf-8'

		chaab = BS(chaab.text, 'html.parser')
		import urllib.parse

		chaab = [urllib.parse.unquote(a.get("href")) for a in chaab.select('div.navbarr > ul > li > a')]

		for a in chaab:
			print("%s ." % a)