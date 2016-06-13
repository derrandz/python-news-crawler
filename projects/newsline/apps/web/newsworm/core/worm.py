# This class shall serve as the heart of our app.
# We will be using htmldom python parser, and the newspaper library.
# 
# My sincere gratitude to anyone that have had a hand in developing these two libraries.

# from newspaper import Article
from .tree import Tree
from .regexr import RegexrClass
from .dom_parser import StaticDomParser as WDom
from .dom_item import DomItem

from newsline.apps.utility.logger.core import logger
from newsline.helpers import helpers
from .divergence import divergent

import re, requests

@divergent("nested_items")
class CrawledItem:
	""" 
		This class would not make sense unless in use in Worm class in conjuction with WDomItem.
		From which arises the reason to put it in the same file, and put its tests in worm_test

		This class serves as a holder of the crawled data, having the data crawled data 
		and its type -WDomItemp- and possible nested data
		as attributes
	"""
	def __init__(self, url, dom_item=None, nested_items=[]):
		self.url = url
		self.dom_item = dom_item
		self.nested_items = []

	@property
	def dom_item(self):
		return self._dom_item

	@dom_item.setter
	def dom_item(self, di):
		if di is not None:
			if not isinstance(di, WDomItem) and not isinstance(di, DomItem):
				if not isinstance(di._original_class, WDomItem) and not isinstance(di._original_class, DomItem):
					raise Exception("[orig: %s ]dom_item must be of type WDomItem, %s given" % (di._original_class, type(di)))
		self._dom_item = di

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
		return "CrawledItemObject{'url': %s}" % (self.url)

	def __str__(self):
		return "CrawledItemObject{'url': %s}" % (self.url)



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
				if not all(isinstance(i, CrawledItem) for i in ci): 
					raise Exception("All elements are expected to be of CrawledItem type, some aren't")
			elif not isinstance(ci, CrawledItem): 
				raise Exception("Expecting CrawledItem or list of CrawledItem, %s given. " % type(ci))

		if not hasattr(self, "_crawled_items"):
			self._crawled_items = []

		self.__add_crawled_item(ci)

	def __add_crawled_item(self, ci):
		def _add_dom_item(crawled_item, di=self):
			if crawled_item.dom_item is None or crawled_item.dom_item != di:
				crawled_item.dom_item = di
			return crawled_item

		if isinstance(ci, list):
			self._crawled_items.extend([_add_dom_item(i) for i in ci]) 
		else:
			self._crawled_items.append(_add_dom_item(ci))

	def __repr__(self):
		return "WDomItemObject{'name': %s, 'url': %s, 'domselector': %s}"	% (self.name, self.url, self.domselector)	

	def __str__(self):
		return "WDomItemObject{'name': %s, 'url': %s, 'domselector': %s}"	% (self.name, self.url, self.domselector)	

	@DomItem.nested_items.setter
	def nested_items(self, ni):
		from newsline.helpers import helpers

		# The initialization case
		if ni is None:
			self._nested_items = []
			return 

		if not hasattr(self, "_nested_items"): self._nested_items = []

		if isinstance(ni, DomItem): self._nested_items.append(ni)
		elif helpers.is_dict(ni):
			try:
				if 'autogen' in ni:
					self._nested_items.append(WDIAutoGen(ni['name'], ni['url'], ni['nested_items'] if 'nested_items' in ni else None, ni['autogen'], ni['range'] if 'range' in ni else None, ni['parentless'] if 'parentless' in ni else False))
				else:
					self._nested_items.append(DomItem(ni['name'], ni['url'], ni['selector'], ni['nested_items']) if 'nested_items' in ni else DomItem(ni['name'], ni['url'], ni['selector']))
			except Exception as e:
				raise Exception("DomItem nested element exception : %s" % str(e))

		elif helpers.is_list(ni):
			if helpers.is_empty(ni): raise Exception("You cannot supply nested_items as empty")
			elif all(isinstance(i, DomItem) or isinstance(i, dict) for i in ni):
				try:
					self._nested_items.extend([(WDIAutoGen(i['name'], i['url'], i['nested_items'] if 'nested_items' in i else None, i['autogen'], i['range'] if 'range' in i else None, i['parentless'] if 'parentless' in i else False) if 'autogen' in i else DomItem(i['name'], i['url'], i['selector'], i['nested_items'] if 'nested_items' in i else None )) if isinstance(i, dict) else i for i in ni]) 
				except Exception as e:
					raise Exception("DomItem nested element exception : %s" % str(e))


class WDIAutoGen(WDomItem):
	""" This is an inheritance to implement a new feature, that is, a dom item can be autogenerated.
		this is a fix for ajax pagination
	"""
	def __init__(self, name, url, nested_items=None, autogen=False, _range=None, parentless=False):
		WDomItem.__init__(self, name, url, 'none', nested_items, [])
		self._is_autogenerated = autogen
		self._is_parentless = parentless
		self._range = _range if _range is not None else [1, 300]

	@property
	def is_autogenerated(self):
		return self._is_autogenerated

	@property
	def is_autogenerated(self):
		return self._is_parentless

	def __repr__(self):
		return "WDomItemObject{'name': %s, 'url': %s, 'is_autogen': %s, 'range': %s, 'is_parenteless': %s}"	% (self.name, self.url, self._is_autogenerated, self._range, self._is_parentless)	

	def __str__(self):
		return "WDomItemObject{'name': %s, 'url': %s, 'is_autogen': %s, 'range': %s, 'is_parenteless': %s}"	% (self.name, self.url, self._is_autogenerated, self._range, self._is_parentless)

	@logger.log_method
	def recognize(self, parentlink):
		"""Return 0 for natural links, 1 for unnatural"""
		part = self.url.replace(parentlink, '')

		if part == self.url:
			self.log("Unnatural: %s" % part)
			return 1
		else: 
			self.log("Natural: %s" % part)
			return 0

	@logger.log_method
	def templify(self, currentparent, parentlink=None):
		if self._is_parentless: return self.url

		if self.recognize(parentlink) == 0:
			return currentparent + self.url.replace(parentlink, '')

		return helpers.templify(self.url, currentparent)

	@logger.log_method
	def generate(self, currentparent, parentlink=None):
		template = self.templify(currentparent, parentlink)
		self.log("Template: %s " % template)
		if template is not None:
			return [template % i for i in range(self._range[0], self._range[1])]
		return None

class Worm(logger.ClassUsesLog):
	# Logging info
	# log_directory_name = "worm_logs"
	# log_name           = "WormClass"
	
	"""
		This class is the core of the newsworm app.
		It is responsible for discovering the right paths to crawl, and extracting the articles from the websites properly.
	"""
	
	def __init__(self, rooturl=None, domitems=None):
		self.regexr = RegexrClass([]) # Explicitly passing an empty list to indicate that this instance will be used as a helper only.
		self.rooturl = rooturl

		# This is called the normalization phase
		# The nesting of the function calls is very important
		self.domitems = self.clean(self.decode(self.normalize(self.validate(domitems))))
		self.patternize()

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
				for i in domitems:
					if 'autogen' in i:
						self._domitems = WDIAutoGen(i['name'], i['url'], i['nested_items'] if 'nested_items' in i else None, i['autogen'], i['range'] if 'range' in i else None, i['parentless'] if 'parentless' in i else False)
					else:
						self._domitems = WDomItem(i['name'], i['url'], i['selector'], i['nested_items'] if 'nested_items' in i else None)
		elif helpers.is_dict(domitems):
			if 'autogen' in domitems:
				self._domitems = WDIAutoGen(domitems['name'], domitems['url'], domitems['nested_items'] if 'nested_items' in domitems else None, domitems['autogen'], domitems['range'] if 'range' in domitems else None, domitems['parentless'] if 'parentless' in domitems else False)
			else:
				self._domitems = WDomItem(domitems['name'], domitems['url'], domitems['selector'], domitems['nested_items'] if 'nested_items' in domitems else None)

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
		if helpers.is_str(domitems): return self.remove_rooturl(domitems)
		elif helpers.is_dict(domitems):
			return helpers.map_dictionary(self.remove_rooturl, domitems, "url")
		elif helpers.is_list(domitems):
			def _mpdictpart(_didict, _func=self.remove_rooturl, _key="url"):
				return helpers.map_dictionary(func=_func, dictionary=_didict, key=_key)

			return list(map(_mpdictpart, domitems))

	def decode(self, domitems):
		""" turns the utf-8/ISO-8859-I arabic characters to unicode arabic characters"""
		if helpers.is_str(domitems): return self.regexr.parse_arabic_urls(domitems)
		elif helpers.is_dict(domitems):
			return helpers.map_dictionary(self.regexr.parse_arabic_urls, domitems, "url")
		elif helpers.is_list(domitems):
			def _mpdictpart(_didict, _func=self.regexr.parse_arabic_urls, _key="url"):
				return helpers.map_dictionary(func=_func, dictionary=_didict, key=_key)

			return list(map(_mpdictpart, domitems))

	def clean(self, domitems):
		""" cleans the urls from the double slashes or trailing slashes"""
		if helpers.is_str(domitems): return self.regexr.remove_double_slash(domitems)
		elif helpers.is_dict(domitems):
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

	def _extract(self, url):
		if not isinstance(url, str): raise Exception("url must be str")
		return WDom(self.clean(self.rooturl + "/" + url))

	def _crawl(self, domitem, inurl, selector=True):
		if not isinstance(domitem, DomItem): raise Exception("__crawl expects to crawl a DomItem Object, %s given" % type(domitem))
		return self._extract(inurl).find(domitem.domselector if selector == True else selector)

	def _crawl_hyperlinks(self, domitem, inurl, force):
		if not isinstance(domitem, DomItem): raise Exception("__crawl expects to crawl a DomItem Object, %s given" % type(domitem))
		def _log_normalize(href) : 
			href = self.clean(self.decode(self.normalize(href)))
			# self.log("Crawled hyperlink :%s" % href)
			return href

		crawled_data = self._crawl(domitem, inurl)
		print("Crawled : %s" % crawled_data)

		if force:
			if not crawled_data:
				crawled_data = self._crawl(domitem, inurl, 'a')
				print("Crawled : %s" % crawled_data)

		return [_log_normalize(hyperlink_tag.get("href")) for hyperlink_tag in crawled_data]

	def _crawl_similar_hyperlinks(self, domitem, inurl, strength=0, force=False):
		if not isinstance(domitem, DomItem): raise Exception("__crawl expects to crawl a DomItem Object, %s given" % type(domitem))

		self.log("Crawling similar hyperlinks for %s" % domitem.name, color="CYAN")

		from functools import partial
		from operator import is_not

		if strength != 'smart':

			def _log_and_match(href):
				self.log("Matching %s" % href)
				if domitem.match(href, strength):
					self.log("Match!", color="GREEN")
					return True
				else:
					self.log("Does not match!", color="RED")
					return False

			return list(filter(partial(is_not, ''), [href if _log_and_match(href) else '' for href in self._crawl_hyperlinks(domitem, inurl, force)]))

		def _log_and_match(href, val): 
			self.log("Matching %s" % href)
			if (val == 0 ) or (val == 1):
				self.log("Match!", color="GREEN")
				return True
			else:
				self.log("Does not match! href = %s" % href, color="RED")
				return False

		return list(filter(partial(is_not, ''), [href if _log_and_match(href, domitem.match(href, strength)) else '' for href in self._crawl_hyperlinks(domitem, inurl, force)]))

	def _pipeout(self, domitem, inurl, strength=0, force=False):
		self.log("Extracting data from %s" % inurl if inurl else self.rooturl, color="DARKCYAN")
		return [CrawledItem(hyperlink) for hyperlink in self._crawl_similar_hyperlinks(domitem, inurl, strength, force)]

	def _pipeout_domitem(self, domitem, inurl, strength=0, force=False):
		pipedout = self._pipeout(domitem, inurl, strength, force)
		self.log("Piping data to %s. Data = %s" % (domitem.name, pipedout), color="YELLOW")
		domitem.crawled_items = pipedout

	def _pipeout_crawled_item(self, crawled_item, strength=0, force=False):
		if crawled_item.dom_item:
			if crawled_item.dom_item.has_nested_items:

				def _setdomitem(domitem, crawleditem):
					crawleditem.dom_item = domitem
					return crawleditem

				self.log("Crawling for [%s] in [%s]." % (crawled_item.dom_item.nested_items[0].name, crawled_item.dom_item.name), color="DARKCYAN")

				for domitem in crawled_item.dom_item.nested_items:
					crawlresults = []
					if not hasattr(domitem, '_is_autogenerated'):
						crawlresults = self._pipeout(domitem, crawled_item.url, strength, force)
					else:
						def is_link_valid(link):
							self.log("[GET][%s]..." % link, color="CYAN")
							from time import sleep
							import requests
							sleep(5)
							request = requests.get(self.clean(self.decode(self.rooturl + "/" + link)))
							if request.status_code == 200:
								self.log("[GET][%s][200]" % link, color="GREEN")
								return CrawledItem(link)
							else:
								self.log("[GET][%s][404]" % link, color="RED")
								return None

						from functools import partial
						from operator import is_not	
						linksl = domitem.generate(crawled_item.url, crawled_item.dom_item.url)
						if linksl is not None:
							crawlresults = list(filter(partial(is_not, None), [is_link_valid(link) for link in linksl]))

					if crawlresults:
						self.log("Crawled %s for %s" % (crawlresults, domitem.name), color="CYAN")
						domitem.crawled_items = crawlresults
						crawled_item.nested_items = [_setdomitem(domitem, ci) for ci in crawlresults]


	def _launch(self, strength=0, force=False):
		from functools import partial
		_potoci = partial(self._pipeout_crawled_item, strength=strength, force=force)

		if not helpers.is_list(self.domitems):
			self._pipeout_domitem(self.domitems, "", strength, force)
		else:
			for di in self.domitems: self._pipeout_domitem(di, "", strength, force)
	
		if not helpers.is_list(self.domitems):
			if not isinstance(self.domitems.crawled_items, list):
				self.domitems.crawled_items.diverge(_potoci)
			else:
				for ci in self.domitems.crawled_items:
					ci.diverge(_potoci)
		else:
			for di in self.domitems:
				if not isinstance(di.crawled_items, list):
					self.domitems.crawled_items.diverge(_potoci)
				else:
					for ci in di.crawled_items:
						ci.diverge(_potoci)

		return self.jsonify()
	
	def jsonify(self):
		def grabtrunk(crawleditem):
			if crawleditem.nested_items:
				def _graball(nesteditems):
					dictt = {}
					for i, ni in enumerate(nesteditems):
						dictt.update({i: grabtrunk(ni)})
					return dictt

				return {
					"item_type"    : crawleditem.dom_item.name,
					"item_url"     : crawleditem.url,
					"nested_items" : _graball(crawleditem.nested_items)
				}

			else:
				print("does not have nested items ")
				return { 
					"item_type"    : crawleditem.dom_item.name,
					"item_url"     : crawleditem.url,
					"nested_items" : "none"
				}

		dictionary = {}
		if helpers.is_list(self.domitems):
			for i, di in enumerate(self.domitems):
				dictionary.update({
						i: {}.update(grabtrunk(ci) for ci in di.crawled_items)
					})
		else:
			for i, ci in enumerate(self.domitems.crawled_items):
				dictionary.update({i: grabtrunk(ci)})

		return dictionary

	def _summary(self):
		def grabtrunk(crawleditem):
			print("grabtrunk for %s" % crawleditem.url)
			if crawleditem.nested_items:
				print("has nested items ")
				def _graball(nesteditems):
					dictt = {}
					for ni in nesteditems:
						dictt.update(grabtrunk(ni))
					return dictt

				return {
					crawleditem.url: {
						"type": crawleditem.dom_item.name,
						"nested_items": _graball(crawleditem.nested_items)
					}
				}
			else:
				print("does not have nested items ")
				return { 
					crawleditem.url :{
						"type": crawleditem.dom_item.name,
						"nested_items": "none"
					}
				}

		summary = {}
		if helpers.is_list(self.domitems):
			for di in self.domitems:
				summary.update({
						di.name: {}.update(grabtrunk(ci) for ci in di.crawled_items)
					})
		else:
			for ci in self.domitems.crawled_items:
				summary.update(grabtrunk(ci))

		return summary