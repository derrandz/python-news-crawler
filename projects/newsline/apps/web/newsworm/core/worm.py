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

from newsline.helpers import helpers as helpers
import re, requests

class Worm:
	"""
	This class is the core of the newsworm app.
	It is responsible for discovering the right paths to crawl, and extracting the articles from the websites properly.
	"""
	from django.conf import settings
	logger = LOGGER.register_class("Worm")
	
	def is_category_multipage(self):
		npup = self.category["nextpage_url"]
		return isinstance(npup, list) and len(npup) > 0

	def crawl(self, url, dom_path=None):
		regxr = self.regexr
		url_pattern = regxr.compile(regxr._regex_url_pattern)

		if url_pattern.match(url):
			DOM = WDom(url)
			if dom_path is not None:
				_dom_path_elements = DOM.find(dom_path)
				return _dom_path_elements
			return DOM

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


		self.root_url = root_url
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

		self.apply_filter()
		self.patternize()
		self.sitemap  = Tree(0, self.root_url, None, True, 0)


	def patternize(self):
		self.category["url_pattern"] = self.patternize_url_category() 
		self.category["article_url_pattern"] = self.patternize_url_article()

		if self.is_category_multipage() :
			self.category["nextpage_url_pattern"] = self.patternize_url_category_nextpage() 


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
					print("Extracting %s from %s"% (self.root_url, urls))
					return rooturl_extractor(urls)
				else:
					raise ValueError("The url must be a list of urls or a string.")
		else:
			self.category["url"] = list(map(rooturl_extractor, self.category["url"]))
			self.category["article_url"] = list(map(rooturl_extractor, self.category["article_url"]))

			if self.is_category_multipage() :
				self.category["nextpage_url"] = list(map(rooturl_extractor, self.category["nextpage_url"]))

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

	def build_report(self):
		return {
			"root_url": self.root_url,
			"category_regex_pattern": self.category["url_pattern"][0],
			"article_regex_pattern": self.category["article_url_pattern"][0],
			"nextpage_regex_pattern": self.category["nextpage_url_pattern"][0] if self.is_category_multipage() else "",
			"results": self.build_tree_dict()
		}

	def launch(self):
		"""
		Applies the supplied training on the supplied root url.
		"""
		self.extract_categories()
		self.extract_articles()
		return self.build_report()

	def extract_categories(self):
		"""
		Gets the links that are specified in the provided dom path
		"""
		safety_flag = True
		categories = self.cdom.find(self.category["dom_path"])

		catlinks  = []
		for category in categories:
			href = self.apply_filter(category.get("href"))
			cu_pattern = self.category["url_pattern"]
			if cu_pattern is not None:
				if cu_pattern[1].match(href):
					catlinks.append(href)
			else:
				safety_flag = False

		# Add the crawled categories links to the sitemap as children
		self.append_categories(catlinks)
		
		if self.is_category_multipage() and safety_flag:
			self.extract_categories_pages()


	def extract_categories_pages(self):
		for category in self.sitemap.children:
			nextpage_dom = self.crawl(self.root_url + "/" + category.content, self.category["nextpage_dom_path"])
			safety_flag = True
			pages = []
			
			for i, page in enumerate(nextpage_dom):
				href = self.apply_filter(page.get("href"))
				npurl_pattern = self.category["nextpage_url_pattern"]
				if npurl_pattern is not None: # Safety check
					if npurl_pattern[1].match(href):
						pages.append(href)
					else:
						print("page did not match")
				else:
					safety_flag = False
			
			if safety_flag:
				if not helpers.is_empty(pages) :
					print("Page %d in %s has : %s" % (i, category.content, pages))
					for page in pages:
						category.add_child(Tree(category.depth + 1, page))


	def extract_articles(self):
		if self.is_category_multipage():
			for category in self.sitemap.children:
				for page in category.children:
					articles_links = self.crawl(self.root_url + "/" + page.content, self.category["article_dom_path"])

					# From the links crawled from the category page, extract the one's who match the provided regex only
					matched_urls = []
					for article_link in articles_links:
						href = self.apply_filter(article_link.get("href"))
						au_pattern = self.category["article_url_pattern"]
						if au_pattern is not None: # Safety check
							if au_pattern[1].match(href):
								matched_urls.append(href)

					# Add the crawled article links to their respective category
					if not helpers.is_empty(matched_urls):
						self.append_articles_to_category(page, matched_urls)
		else:
			# Get all the links in the page of the category
			for category in self.sitemap.children:
				articles_links = self.crawl(self.root_url + "/" + category.content, self.category["article_dom_path"])

				# From the links crawled from the category page, extract the one's who match the provided regex only
				matched_urls = []
				for article_link in articles_links:
					href = self.apply_filter(article_link.get("href"))
					au_pattern = self.category["article_url_pattern"]
					if au_pattern is not None: # Safety check
						if au_pattern[1].match(href):
							matched_urls.append(href)

				# Add the crawled article links to their respective category
				self.append_articles_to_category(category, matched_urls)


	def append_categories(self, catlinks, url_prefix=None):
		"""
		Builds a hiarchical view of the site, a map of links.
		This function adds the second level that is of categories.
		"""
		assert isinstance(catlinks, list)

		if url_prefix is None: url_prefix = self.root_url

		links = []
		for link in catlinks:
			full_link = url_prefix + "/" + link
			print("Is link valid : %s from %s"%(full_link, link))
			if self.is_link_valid(full_link):
				links.append(link)

		print("Appending: OK!")
		for link in links:
			self.sitemap.add_child(Tree(self.sitemap.depth + 1, link))

	def remove_categoy(self, tbr_category):
		for index, category in enumerate(self.sitemap.children):
			if category.content == tbr_category.content:
				del category.children[:]
				del self.sitemap.children[index]

	def append_articles_to_category(self, catnode, artlinks):
		"""
		Builds a hiarchical view of the site, a map of links.
		This function adds the second level that is of categories.
		"""
		assert isinstance(artlinks, list)
		if not len(artlinks) > 0 :
			self.remove_categoy(catnode)
		else:
			links = []
			for link in artlinks:
				full_link = self.root_url + "/" + link
				if self.is_link_valid(full_link):
					links.append(link)

			for link in links:
				catnode.add_child(Tree(self.sitemap.tree_depth_size + 2, link))

	def is_link_valid(self, link):
		r = requests.get(link)
		if r.status_code != 200:
			return False
		else:
			return True

	def patternize_url(self, urls):
		"""
		This method will extract the regex pattern of the url as to get all similar links.
		"""
		if isinstance(urls, list):
			patterns = "("
			if len(urls) > 1:
				for index, url in enumerate(urls):
					if index == len(urls) - 1:
						patterns += self.regexr.make_pattern(url)[0] + ")"
					else:
						patterns += self.regexr.make_pattern(url)[0] + "|"
					index += 1

				return [patterns, re.compile(patterns, re.IGNORECASE|re.DOTALL)]
			else:
				return self.regexr.make_pattern(urls[0], True)

		elif isinstance(urls, str):
			return self.regexr.make_pattern(urls, True)

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