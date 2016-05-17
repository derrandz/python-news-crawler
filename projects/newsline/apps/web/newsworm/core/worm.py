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
	
	def __init__(self, root_url=None, category=None):
		"""
		Worm.__init__ instantiates a worm instance with a target url.
		Using this url, the worm will perform a recursive crawl to draw a hiarchical map of the website's gateways.
		The recursive crawl will detect the "article depth", the depth at which the articles reside.

		Make sure the url provided is a root url, or something of the kind subdomain.url.com
		Make sure the prefix of the url is http://
		"""
		def has_expected_keys(keys):
			for key in keys:
				if not key in category:
					raise ValueError("The key %s was not found, make sure you specified it." % key)

		def are_lists(keys):
			for key in keys:
				if not isinstance(category[key], list):
					if key != "category_nextpage_url":
						raise ValueError("%s is not a list, list expected" % key)

		def are_lists_empty(keys):
			for key in keys:
				if not len(category[key]) > 0 : 
					if key != "category_nextpage_url": 
						raise ValueError("list %s can not be empty" % key)

		def are_strings(keys):
			for key in keys:
				if not isinstance(category[key], str):
					raise ValueError("%s is not a string, string expected" % key)

		def are_strings_empty(keys):
			for key in keys:
				if category[key] == "":
					if key != "category_nextpage_dom_path":
						raise ValueError("You cannot supply an empty string at %s " % key)
		
		expected_keys       = ["category_url","category_dom_path", "category_nextpage_url", "category_nextpage_dom_path", "category_article_url", "category_article_dom_path"]
		expected_as_lists   = ["category_url", "category_nextpage_url", "category_article_url"]
		expected_as_strings = ["category_dom_path", "category_nextpage_dom_path", "category_article_dom_path"]

		if root_url is None:
			raise ValueError("root_url can not be None.")
		else:
			if root_url == "":
				raise ValueError("root_url can not be an empty string")

		has_expected_keys(expected_keys)
		are_lists(expected_as_lists)
		are_lists_empty(expected_as_lists)
		are_strings(expected_as_strings)
		are_strings_empty(expected_as_strings)


		self.root_url = root_url.strip("/")
		self.regexr   = RegexrClass()
		self.cdom     = self.crawl(self.root_url)
		self.category = {
							"url": category["category_url"],
							"dom_path": category["category_dom_path"], 
							"url_pattern": "", 
							"nextpage_url": category["category_nextpage_url"] , # That is a list containing one or more url
							"nextpage_dom_path": category["category_nextpage_dom_path"] if not helpers.is_empty(category["category_nextpage_url"]) else "", 
							"nextpage_url_pattern": "", 
							"article_url": category["category_article_url"], 
							"article_dom_path": category["category_article_dom_path"], 
							"article_url_pattern": ""
						}

		self.log("Worm has been initialized with following parameters \n:")
		for key, value in self.category.items():
			self.log("%s  : \n%s" % (key, value))
		
		self.apply_filter()
		self.decode_arabic_urls()
		self.patternize()

		self.sitemap  = Tree(0, self.root_url, None, True, 0)

	def is_category_multipage(self):
		npup = self.category["nextpage_url"]
		return isinstance(npup, list) and len(npup) > 0

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

	def get_report(self):
		crawled_categories_count = len(self.sitemap.children)
		crawled_pages_count      = 0
		crawled_articles_count   = 0

		failed_categories_count  = 0
		success_categories_count = 0

		if self.is_category_multipage():
			failed_pages_count  = 0
			success_pages_count = 0
			if not helpers.is_empty(self.sitemap.children):
				for category in self.sitemap.children:
					if helpers.is_empty(category.children):
						failed_categories_count += 1
					else:
						crawled_pages_count += len(category.children)
						for page in category.children:
							if helpers.is_empty(page.children):
								failed_pages_count += 1
							else:
								success_pages_count += 1
								crawled_articles_count += len(page.children)

			return ""
		else:
			if not helpers.is_empty(self.sitemap.children):
				for category in self.sitemap.children:
					if helpers.is_empty(category.children):
						failed_categories_count += 1
					else:
						success_categories_count += 1
						crawled_articles_count += len(category.children)


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
		return self.root_url + self.regexr.remove_double_slash(url)