# This class shall serve as the heart of our app.
# We will be using htmldom python parser, and the newspaper library.
# 
# My sincere gratitude to anyone that have had a hand in developing these two libraries.

# from newspaper import Article
from .tree import Tree
from .regexr import RegexrClass
from .dom_parser import WormDomParser as WDom
from .dom_item import DomItem

from newsline.apps.utility.logger.core import logger
from newsline.helpers import helpers

import re, requests

class CrawledItem:
	""" 
		This class would not make sense unless in use in Worm class in conjuction with WDomItem.
		From which arises the reason to put it in the same file, and put its tests in worm_test

		This class serves as a holder of the crawled data, having the data crawled data 
		and its type -WDomItemp- and possible nested data
		as attributes
	"""
	def __init__(self, crawled_data, dom_item=None, nested_items=[]):
		self.crawled_data = crawled_data
		self.dom_item = dom_item
		self.nested_items = []

	@property
	def dom_item(self):
		return self._dom_item

	@dom_item.setter
	def dom_item(self, di):
		if di is not None:
			if not isinstance(di, WDomItem): raise Exception("dom_item must be of type WDomItem, %s given" % type(di))
		self._dom_item = di

		if self._dom_item is not None:
			if not self in self._dom_item.crawled_items:
				self._dom_item.crawled_items.append(self)
	
	@property
	def nested_items(self):
		return self._nested_crawled_items

	@nested_items.setter
	def nested_items(self, nci):
		if isinstance(nci, list): 
			if not all(isinstance(i, CrawledItem) for i in nci): raise Exception("nested_items must be all of type CrawledItem, some aren't")
		elif not isinstance(nci, CrawledItem): raise Exception("Expecting CrawledItem or list of CrawledItems, %s given" % type(nci))
		self._nested_crawled_items = nci
	
	def __repr__(self):
		return "{'crawled_data': %s, 'dom_item': %s, 'nested_items': %s}" % (self.crawled_data, self.dom_item, self.nested_items)

	def __str__(self):
		return "{'crawled_data': %s, 'dom_item': %s, 'nested_items': %s}" % (self.crawled_data, self.dom_item, self.nested_items)

class WDomItem(DomItem):
	""" This is an inheritance to implement a new feature, that is, each DomItem has many crawled items"""
	def __init__(self, name, url, domselector, nested_items=None, crawled_items=[]):
		DomItem.__init__(self, name, url, domselector, nested_items)
		self.crawled_items = crawled_items

	@property
	def crawled_items(self):
		return self._crawled_items

	@crawled_items.setter
	def crawled_items(self, ci):
		if ci:
			if isinstance(ci, list):
				if not all(isinstance(i, DomItem) for i in ci): 
					raise Exception("All elements are expected to be of CrawledItem type, some aren't")
			elif not isinstance(ci, CrawledItem): 
				raise Exception("Expecting CrawledItem or list of CrawledItem, %s given. " % type(ci))

		if not hasattr(self, "_crawled_items"):
			self._crawled_items = []

		self.__add_crawled_item(ci)

	def __add_crawled_item(self, ci):
		def _add_dom_item(crawled_item, di=self):
			crawled_item.dom_item = di
			return crawled_item

		if isinstance(ci, list): 
			self._crawled_items.extend([_add_dom_item(i) for i in ci]) 
		else:
			self._crawled_items.append(_add_dom_item(ci))
	
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
		self.regexr = RegexrClass([]) # Explicitly passing an empty list to indicate that this instance will be used for helpers method only.
		self.rooturl = rooturl

		# This is called the normalization phase
		# The nesting of the function calls is very important
		self.domitems = self.clean(self.decode(self.normalize(self.validate(domitems))))
		self.patternize()

		self.init_sitemap()

	@property
	def sitemap(self):
		return self._sitemap
	
	@sitemap.setter
	def sitemap(self, sm):
		if not isinstance(sm, Tree): raise Exception("Sitemap expects a tree node object, %s given" % type(sm))
		self._sitemap = sm

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

	def validate(self, domitems):
		if helpers.is_list(domitems):
			if not all(helpers.is_dict(di) for di in domitems):
				raise Exception("The domitems list expects all elements to be dictionaries, some aren't")
			else:
				return domitems
		else:
			if not helpers.is_dict(domitems):
				raise Exception("The domitems expects a dictionary element, %s given" % type(domitems))
			else:
				return domitems

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
			for item in self.domitems:
				item.patternize()
		elif isinstance(self.domitems, DomItem):
			self.domitems.patternize()

	def init_sitemap(self):
		self.sitemap = Tree(self.rooturl, 0)

	def _extract(self, url):
		if not isinstance(url, str): raise Exception("url must be str")
		return WDom(self.rooturl + "/" + url)

	def _crawl(self, domitem):
		if not isinstance(domitem, DomItem): raise Exception("__crawl expects to crawl a DomItem Object, %s given" % type(domitem))
		return self._extract(domitem.url).find(domitem.domselector)

	def _crawl_hyperlinks(self, domitem):
		if not isinstance(domitem, DomItem): raise Exception("__crawl expects to crawl a DomItem Object, %s given" % type(domitem))
		return [hyperlink_tag.get("href") for hyperlink_tag in self._crawl(domitem)]

	def _crawl_similar_hyperlinks(self, domitem, strength=0):
		if not isinstance(domitem, DomItem): raise Exception("__crawl expects to crawl a DomItem Object, %s given" % type(domitem))
		from functools import partial
		from operator import is_not
		if strength != 'smart':
			return list(filter(partial(is_not, ''), [href if domitem.match(href, strength) else '' for href in self._crawl_hyperlinks(domitem)]))

		def _matches(val): return True if (val == 0 ) or (val == 1) else False
		return list(filter(partial(is_not, ''), [href if _matches(domitem.match(href, strength)) else '' for href in self._crawl_hyperlinks(domitem)]))

	def crawl(self):
		if not isinstance(self.domitems, list):
			self.domitems.crawled_items = self._crawl_similar_hyperlinks(self.domitems)
			if self.domitems.has_nested_items
		else: