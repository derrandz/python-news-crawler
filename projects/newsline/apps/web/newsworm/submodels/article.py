from .website import WebsiteChild
from django.db import models

class Article(WebsiteChild):
	url          = models.CharField(max_length=255) 
	page         = models.CharField(max_length=255)
	authors      = models.CharField(max_length=255, blank=True, null=True)
	keywords     = models.CharField(max_length=255, blank=True, null=True)
	category     = models.CharField(max_length=255)

	crawl_date   = models.DateTimeField(auto_now=False, auto_now_add=False, blank=True, null=True)
	publish_date = models.DateTimeField(auto_now=False, auto_now_add=False, blank=True, null=True)

	def __str__(self):
		return "url: %s, page: %s, category: %s, keywords: %s, authors: %s, crawl_date: %s, publish_date: %s, website: %s" % (self.url, self.page, self.category, self.keywords, self.authors, self.crawl_date, self.publish_date, self.website.name)