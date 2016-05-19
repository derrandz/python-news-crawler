# This class shall serve as the heart of our app.
# We will be using htmldom python parser, and the newspaper library.
# 
# My sincere gratitude to anyone that have had a hand in developing these two libraries.

# from newsline.apps.web.newsworm.submodels. import NewswormArticle
from newspaper import Article
from htmldom import htmldom
from .tree import Tree
from .regexr import RegexrClass
from .dom_parser import WormDomParser as WDom

from newsline.apps.utility.logger.core import logger
from newsline.helpers import helpers

import re, requests

@logger.log_class
class Worm(logger.ClassUsesLog):
	# Logging info
	log_directory_name = "worm_logs"
	log_name           = "WormClass"
	
	"""
	This class is the core of the newsworm app.
	It is responsible for discovering the right paths to crawl, and extracting the articles from the websites properly.
	"""
	
	def __init__(self, rooturl=None, domitems=None):
		self.regexr = RegexrClass()
		self.rooturl = rooturl

		# cleans and normalizes the data that will create the dom items
		self.domitems = self.clean(self.decode(self.normalize(domitems)))
		self.patternize()

		# self.sitemap  = Tree(0, self.root_url, None, True, 0)
		# self.cdom = self.crawl(self.root_url)

	@property
	def regexr(self):
		if not self._regexr or self._regexr is None:
			self.regexr = RegexrClass()
		return self._regexr

	@regexr.setter
	def regexr(self, value):
		regexrType = type(RegexrClass())
		if not isinstance(value, regexrType): raise Exception("You can not reinitialize the regexr to something other than RegexrClass")
		self._regexr = value


	@property
	def rooturl(self):
		return self._rooturl

	@rooturl.setter
	def rooturl(self, url):
		if not url or url is None: raise Exception("rooturl cannot be empty or None")
		if helpers.is_str(url): 
			if not helpers.is_url(url): 
				raise Exception("rooturl should respect the form a url e.g: http://google.com\n\t url: %s"% url)
		if helpers.is_list(url):
			if helpers.is_empty(url):
				raise Exception("rooturl list can not be empty")
			elif not all(helpers.is_str(u) for u in url):
				raise Exception("rooturl is list, expecting all list elements to be str, however an element (or more) is not")
			elif not helpers.is_url(url, root=True):
				raise Exception("rooturl list given, however an element does not respect url pattern. e.g: http://google.com\n\t url: %s"% url)

		if helpers.is_str(url):
			self._rooturl = url.strip("/")
		elif helpers.is_list(url):
			def _strip(u, dl):
				return u.strip(dl)

			self._rooturl = [_strip(u, "/") for u in url]

	@property
	def domitems(self):
		return self._domitems

	@domitems.setter
	def domitems(self, domitems):
		if helpers.is_list(domitems):
			if not all(helpers.is_dict(domitem) for domitem in domitems):
				raise Exception("The domitems list expects all elements to be dictionaries, some aren't")
			else:
				self._domitems = [DomItem(i['name'], i['url'], i['selector'], i['nested_items']) if 'nested_items' in i else DomItem(i['name'], i['url'], i['selector']) for i in domitems]
		elif helpers.is_dict(domitems):
			self._domitems = DomItem(domitems['name'], domitems['url'], domitems['selector'], domitems['nested_items']) if 'nested_items' in domitems else DomItem(domitems['name'], domitems['url'], domitems['selector'])

	def remove_rooturl(self, url):
		return self.regexr.del_substring(self.rooturl, url)

	def normalize(self, domitems):
		""" removes the rooturl from the domitem urls if they have it"""
		if helpers.is_dict(domitems):
			return helpers.map_dictionary(self.remove_rooturl, domitems, "url")
		elif helpers.is_list(domitems):
			def _mpdictpart(_didict, _func=self.remove_rooturl, _key="url"):
				return helpers.map_dictionary(func=_func, dictionary=_didict, key=_key)

			return list(map(_mpdictpart, domitems))

	def decode(self, domitems):
		""" turns the utf-8 arabic characters to unicode arabic characters"""
		if helpers.is_dict(domitems):
			return helpers.map_dictionary(self.regexr.parse_arabic_urls, domitems, "url")
		elif helpers.is_list(domitems):
			def _mpdictpart(_didict, _func=self.regexr.parse_arabic_urls, _key="url"):
				return helpers.map_dictionary(func=_func, dictionary=_didict, key=_key)

			return list(map(_mpdictpart, domitems))

	def clean(self, domitems):
		""" cleans the urls from the double slashes or trailing slashes"""
		if helpers.is_dict(domitems):
			return helpers.map_dictionary(self.regexr.remove_double_slash, domitems, "url")
		elif helpers.is_list(domitems):
			def _mpdictpart(_didict, _func=self.regexr.remove_double_slash, _key="url"):
				return helpers.map_dictionary(func=_func, dictionary=_didict, key=_key)

			return list(map(_mpdictpart, domitems))

	def patternize(self):
		if helpers.is_list(self.domitems):
			useless_container = [ x.method_call() for x in a_list_of_objects ]
		elif isinstance(self.domitems, DomItem):
			self.domitems.patternize()