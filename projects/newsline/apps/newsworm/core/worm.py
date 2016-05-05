# This class shall serve as the heart of our app.
# We will be using htmldom python parser, and the newspaper library.
# 
# My sincere gratitude to anyone that have had a hand in developing these two libraries.

from ..submodels.newsworm_article import NewswormArticle
from newspaper import Article
from htmldom import htmldom
from .tree import Tree
from .regexr import RegexrClass

import re, requests

class Worm:
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
		
		self.sitemap  = Tree(0, root_url)
		self.root_url = root_url
		self.regexr   = RegexrClass()

		assert isinstance(category["category_url"], list)
		self.category = {
							"url": category["category_url"], # That is a list containing one or more url
							"category_dom_path": category["category_dom_path"], 
							"pattern": "", 
							"category_article_url": category["category_article_url"], 
							"article_dom_path": category["article_dom_path"], 
							"article_url_pattern": ""
						}

	def launch():
		"""
		Applies the supplied training on the supplied root url.
		"""
		self.extract_categories()
		self.extract_articles()


	def find_in_sitemap(index, depth=None):
		if depth is not None:
			if depth == self.sitemap.depth + 1:
				for catnode in self.sitemap.children:
					if catnode.content == index:	return catnode

			elif depth == self.sitemap.depth + 2:
				for catnode in self.sitemap.children:
					for articlenode in catnode.children:
						if articlenode.content == index:	return articlenode

		return None


	def extract_categories(self):
		"""
		Gets the links that are specified in the provided dom path
		"""

		categories = htmldom.HtmlDom(self.root_url).createDom().find(self.category["dom_path"])
		catlinks  = []
		for category in categories:
			catlinks.append(category.attr("href"))

		self.append_categories(catlinks)


	def extract_articles(self):
		articles = {}
		# Get all the links in the page of the category
		for category in self.sitemap.children:
			articles_links = htmldom.HtmlDom(category["url"]).createDom().find("a")

			# From the links crawled from the category page, extract the one's who match the provided regex only
			for article_link in article_links:
				p = re.compile(category["article_url_pattern"])

				if p.search(article_link):
					if(_.group(0) == article_link): 
						articles[category["url"]] = article_link.attr("href")

			# Add the crawled article links to their respective category
			self.append_articles_to_category(catnode, articles, category.content)


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
			if self.is_link_valid(full_link):
				links.append(full_link)

		for link in links:
			self.sitemap.add_child(Tree(self.sitemap.depth + 1, link))


	def append_articles_to_category(self, catnode, artlinks):
		"""
		Builds a hiarchical view of the site, a map of links.
		This function adds the second level that is of categories.
		"""
		assert isinstance(artlinks, list)

		links = []
		for link in artlinks:
			full_link = url_prefix + "/" + link
			if self.is_link_valid(full_link):
				links.append(full_link)

		for link in links:
			catnode.add_child(Tree(self.sitemap.depth + 2, link))


	def is_link_valid(self, link):
		r = requests.get(link)
		if r.status_code != 200:
			return False
		else:
			return True


	def patternize_url_category(self):
		"""
		This method will extract the regex pattern of the url as to get all similar links.
		This will helps us extract all the links of articles in a website.

		"""
		patterns = "("
		if len(self.category["url"]) > 1:
			for index, url in enumerate(self.category["url"]):
				if index == len(self.category["url"]) - 1:
					patterns += self.regexr.make_pattern(url)[0] + ")"
				else:
					patterns += self.regexr.make_pattern(url)[0] + "|"
				index += 1

			return [patterns, re.compile(patterns, re.IGNORECASE|re.DOTALL)]
		else:
			return self.regexr.make_pattern(self.category["url"][0], True)	

	def patternize_url_article(self):
		"""
		This method will extract the regex pattern of the url as to get all similar links.
		This will helps us extract all the links of articles in a website.

		"""
		patterns = "("
		if len(self.category["category_article_url"]) > 1:
			for index, url in enumerate(self.category["category_article_url"]):
				if index == len(self.category["category_article_url"]) - 1:
					patterns += self.regexr.make_pattern(url)[0] + ")"
				else:
					patterns += self.regexr.make_pattern(url)[0] + "|"
				index += 1

			return [patterns, re.compile(patterns, re.IGNORECASE|re.DOTALL)]
		else:
			return self.regexr.make_pattern(self.category["category_article_url"][0], True)	

