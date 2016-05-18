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
		self.rooturl = rooturl
		self.domitems = domitems

		self.cdom     = self.crawl(self.root_url) if not nocrawl else ""
		
		self.apply_filter()
		self.decode_arabic_urls()
		self.patternize()

		self.sitemap  = Tree(0, self.root_url, None, True, 0)

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

		self._rooturl = url

	@property
	def domitems(self):
		return self._domitems

	@domitems.setter
	def domitems(self, domitems):
		if heplers.is_list(domitems):
			if not all(helpers.is_dict(domitem) for domitem in domitems):
				raise Exception("The domitems list expects all elements to be dictionaries, some aren't")
			else:
				self._domitems = [DomItem(i['name'], i['url'], i['selector'], i['nested_items']) if 'nested_items' in i else DomItem(i['name'], i['url'], i['selector']) for i in domitems]
		elif helpers.is_dict(domitems):
			self._domitems = DomItem(domitems['name'], domitems['url'], domitems['selector'], domitems['nested_items']) if 'nested_items' in domitems else DomItem(domitems['name'], domitems['url'], domitems['selector'])

	@logger.log_method
	def crawl(self, url, dom_path=None):
		if dom_path is not None:
			return WDom(url).find(dom_path)
		else:
			return WDom(url)

	def patternize(self):
		self.category["url_pattern"] = self.patternize_url_category() 
		self.category["article_url_pattern"] = self.patternize_url_article()

		if self.is_category_multipage() :
			self.category["nextpage_url_pattern"] = self.patternize_url_category_nextpage() 

	def decode_arabic_urls(self, urls=None):
		if urls is not None:
			if helpers.is_list(urls):
				return list(map(self.regexr.parse_arabic_urls, urls))
			else:
				if helpers.is_str(urls):
					return self.regexr.parse_arabic_urls(urls)
				else:
					raise ValueError("The url must be a list of urls or a string.")
		else:
			self.category["url"] = list(map(self.regexr.parse_arabic_urls, self.category["url"]))
			self.category["article_url"] = list(map(self.regexr.parse_arabic_urls, self.category["article_url"]))

			if self.is_category_multipage() :
				self.category["nextpage_url"] = list(map(self.regexr.parse_arabic_urls, self.category["nextpage_url"]))

	def apply_filter(self, urls=None):
		def url_extractor(_substring, _string):
			return self.regexr.del_substring(_substring, _string)

		def rooturl_extractor(_string):
			return url_extractor(self.root_url, _string)

		if urls is not None:
			if helpers.is_list(urls):
				return list(map(rooturl_extractor, urls))
			else:
				if helpers.is_str(urls):
					return rooturl_extractor(urls)
				else:
					raise ValueError("The url must be a list of urls or a string.")
		else:
			self.category["url"] = list(map(rooturl_extractor, self.category["url"]))
			self.category["article_url"] = list(map(rooturl_extractor, self.category["article_url"]))

			if self.is_category_multipage() :
				self.category["nextpage_url"] = list(map(rooturl_extractor, self.category["nextpage_url"]))

	@logger.log_method
	def launch(self):
		"""
		Applies the supplied training on the supplied root url.
		"""
		self.extract_categories()
		self.extract_articles()
		return self.build_report()

	def matches_category(self, link):
		if self.category["url_pattern"] is not None:
			if self.category["url_pattern"][1].match(link):
				return link

	def matches_nextpage(self, link):
		if self.category["nextpage_url_pattern"] is not None:
			if self.category["nextpage_url_pattern"][1].match(link):
				return link

	def matches_articles(self, link):
		if self.category["article_url_pattern"] is not None:
			if self.category["article_url_pattern"][1].match(link):
				return link

	def extract_href(self, dom_el):
		return dom_el.get("href")

	@logger.log_method
	def extract_categories(self):
		"""
		Gets the links that are specified in the provided dom path
		"""
		dom_categories          = self.cdom.find(self.category["dom_path"])
		self.log("dom_categories: \n%s" % dom_categories)

		href_categories         = list(map(self.extract_href, dom_categories)) # Returns hrefs from dom elements
		self.log("href_categories: \n%s" % href_categories)

		clean_href_categories   = list(map(self.apply_filter, href_categories)) # removes http://root.com from href if it exists
		self.log("clean_href_categories: \n%s" % clean_href_categories)

		decoded_href_categories = list(map(self.decode_arabic_urls, clean_href_categories)) # if url is arabic, parses it to arabic chars
		self.log("decoded_href_categories: \n%s" % decoded_href_categories)

		matched_categories      = list(map(self.matches_category, decoded_href_categories)) # returns an array of urls that match the category url pattern
		self.log("matched_categories: \n%s" % matched_categories)

		# Add the crawled categories links to the sitemap as children
		if not helpers.is_empty(matched_categories):
			self.append_categories(matched_categories)
		else:
			self.log("Could not find any category that respects the generated Regex")
		
		if self.is_category_multipage():
			self.extract_categories_pages()

	@logger.log_method
	def extract_categories_pages(self):
		for category in self.sitemap.children:

			nextpage_dom = self.crawl(self.add_rooturl(category.content), self.category["nextpage_dom_path"])

			self.log("nextpage_dom: \n%s" % nextpage_dom)

			nextpage_href = list(map(self.extract_href, nextpage_dom))
			self.log(" nextpage_href: \n%s" % nextpage_href)

			clean_href_nextpage   = list(map(self.apply_filter, nextpage_href)) # removes http://root.com from href if it exists
			self.log(" clean_href_nextpage: \n%s" % clean_href_nextpage)

			nextpage_decoded = list(map(self.decode_arabic_urls, clean_href_nextpage))
			self.log(" nextpage_decoded: \n%s" % nextpage_decoded)

			matched_pages = list(map(self.matches_nextpage, nextpage_decoded))
			self.log(" nextpage_matched_pages: \n%s" % matched_pages)

			if not helpers.is_empty(matched_pages) :
				for page in matched_pages:
					if page is not None:
						category.add_child(Tree(category.depth + 1, page))
			else:
				self.log("Could not find any next pages linsk for category %s" % category.content)	

	@logger.log_method
	def extract_articles(self):
		is_category_multipage = self.is_category_multipage()
		if is_category_multipage:
			self.log(" Website is multipage per category")
			for category in self.sitemap.children:
				self.log(" Category %s contains: %s \n" % (category.content, category.children))
				for page in category.children:
					self.log(" Extracting articles from page : %s, for category %s \n" % (page.content, category.content))

					articles_dom           = self.crawl(self.add_rooturl(page.content), self.category["article_dom_path"])
					self.log(" articles_dom: \n%s" % articles_dom)

					articles_hrefs         = list(map(self.extract_href, articles_dom))
					self.log(" articles_hrefs: \n%s" % articles_hrefs)

					clean_href_articles   = list(map(self.apply_filter, articles_hrefs)) # removes http://root.com from href if it exists
					self.log(" clean_href_articles: \n%s" % clean_href_articles)

					decoded_articles_hrefs = list(map(self.decode_arabic_urls, clean_href_articles))
					self.log(" decoded_articles_hrefs: \n%s" % decoded_articles_hrefs)

					matched_urls = list(map(self.matches_articles, decoded_articles_hrefs))
					self.log(" matched_urls: \n%s" % matched_urls)

					# Add the crawled article links to their respective category
					if not helpers.is_empty(matched_urls):
						self.append_articles_to_category(page, matched_urls)
					else:
						self.log("Could not find any articles in page: %s, category: %s"% (category.content, page.content))
		else:
			for category in self.sitemap.children:
				self.log(" Extracting articles from page : %s, for category %s \n" % (page.content, category.content))

				articles_dom           = self.crawl(self.add_rooturl(category.content), self.category["article_dom_path"])
				self.log(" articles_dom: \n%s" % articles_dom)

				articles_hrefs         = list(map(self.extract_href, articles_dom))
				self.log(" articles_hrefs: \n%s" % articles_hrefs)

				clean_href_articles   = list(map(self.apply_filter, articles_hrefs)) # removes http://root.com from href if it exists
				self.log(" clean_href_articles: \n%s" % clean_href_articles)

				decoded_articles_hrefs = list(map(self.decode_arabic_urls, clean_href_articles))
				self.log(" decoded_articles_hrefs: \n%s" % decoded_articles_hrefs)

				matched_urls = list(map(self.matches_articles, decoded_articles_hrefs))
				self.log(" matched_urls: \n%s" % matched_urls)

				# Add the crawled article links to their respective category
				if not helpers.is_empty(matched_urls):
					self.append_articles_to_category(category, matched_urls)
				else:
					self.log("Could not find any articles in page: %s, category: %s"% (category.content, page.content))

	@logger.log_method
	def append_categories(self, catlinks, url_prefix=None):
		"""
		Builds a hiarchical view of the site, a map of links.
		This function adds the second level that is of categories.
		"""
		assert isinstance(catlinks, list)

		for link in catlinks:
			if link is not None:
				self.sitemap.add_child(Tree(self.sitemap.depth + 1, link))

	@logger.log_method
	def remove_categoy(self, tbr_category):
		for index, category in enumerate(self.sitemap.children):
			if category.content == tbr_category.content:
				del category.children[:]
				del self.sitemap.children[index]

	@logger.log_method
	def append_articles_to_category(self, catnode, artlinks):
		"""
		Builds a hiarchical view of the site, a map of links.
		This function adds the second level that is of categories.
		"""
		assert isinstance(artlinks, list)
		if not len(artlinks) > 0 :
			self.remove_categoy(catnode)
		else:
			for link in artlinks:
				if link is not None:
					catnode.add_child(Tree(self.sitemap.tree_depth_size + 2, link))

	def is_link_valid(self, link):
		r = requests.get(self.decode_arabic_urls(link))
		if r.status_code != 200:
			return False
		else:
			return True

	def patternize_url(self, urls):
		"""
		This method will extract the regex pattern of the url as to get all similar links.
		"""
		if isinstance(urls, list):
			if helpers.is_empty(list):
				return None

			patterns = "("
			if len(urls) > 1:
				for index, url in enumerate(urls):
					if index == len(urls) - 1:
						patterns += self.regexr.make_pattern(url)[0] + ")"
					else:
						patterns += self.regexr.make_pattern(url)[0] + "|"
					index += 1

				patternsReturn = [patterns, re.compile(patterns, re.IGNORECASE|re.DOTALL)]
				return patternsReturn
			else:
				patternsReturn = self.regexr.make_pattern(urls[0], True)
				return patternsReturn

		elif isinstance(urls, str):
			patterns = self.regexr.make_pattern(urls, True)
			return patterns
		else:
			return None

	def patternize_url_category(self):
		"""
		This method will extract the regex pattern of the url as to get all similar links.
		This will helps us extract all the links of articles in a website.

		"""
		return self.patternize_url(self.category["url"])

	def patternize_url_article(self):
		"""
		This method will extract the regex pattern of the url as to get all similar links.
		This will helps us extract all the links of articles in a website.

		"""
		return self.patternize_url(self.category["article_url"])

	def patternize_url_category_nextpage(self):
		"""
		This method will extract the regex pattern of the url as to get all similar links.
		This will helps us extract all the links of articles in a website.

		"""
		return self.patternize_url(self.category["nextpage_url"])

	def build_tree_dict(self):
		tree_dict = {}
		if self.is_category_multipage():
			for category in self.sitemap.children:
				pages_list = {}
				for page in category.children:
					aritcles_list = []
					for article in page.children:
						aritcles_list.append(article.content)

					pages_list.update({page.content: aritcles_list})

				tree_dict.update({category.content: pages_list})
		else:
			for category in self.sitemap.children:
				aritcles_list = [] # A list for urls
				for article in category.children:
					aritcles_list.append(article.content)
				tree_dict.update({category.content: aritcles_list})

		return tree_dict

	def get_status(self):
		if self.is_category_multipage():
			if helpers.is_empty(self.sitemap.children):
				return False
			else:
				for category in self.sitemap.children:
					if helpers.is_empty(category.children):
						return False
					else:
						for page in category.children:
							if helpers.is_empty(page.children):
								return False
		else:
			if helpers.is_empty(self.sitemap.children):
				return False
			else:
				for category in self.sitemap.children:
					if helpers.is_empty(category.children):
						return False
		return True

	def build_report(self):
		tree_dict = self.build_tree_dict()
		self.close_logging_session()
		return {
			"root_url": self.root_url,
			"category_regex_pattern": self.category["url_pattern"][0],
			"article_regex_pattern": self.category["article_url_pattern"][0],
			"nextpage_regex_pattern": self.category["nextpage_url_pattern"][0] if self.is_category_multipage() else "",
			"results": tree_dict,
			"status" : self.get_status(),
			"report" : self.get_report()
		}

	def add_rooturl(self, url):
		url = self.regexr.remove_double_slash(url)
		if url[0] == "/" :
			return self.root_url + url
		else:
			return self.root_url + "/" + url 