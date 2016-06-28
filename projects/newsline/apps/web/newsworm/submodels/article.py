from .website import Crawl
from django.db import models
from .abstract_model import ANewswormModel

class Article(ANewswormModel):
	url          = models.CharField(max_length=255) 
	crawl        = models.ForeignKey(Crawl, on_delete=models.CASCADE)
	title        = models.CharField(max_length=255, blank=True, null=True)
	content      = models.TextField()
	authors      = models.CharField(max_length=255, blank=True, null=True)
	keywords     = models.CharField(max_length=255, blank=True, null=True)
	topimage_url = models.CharField(max_length=255) 
	publish_date = models.CharField(max_length=255) 
	
	def __str__(self):
		return "url: %s, title: %s, keywords: %s, authors: %s, publish_date: %s" % (self.url, self.title, self.keywords, self.authors, self.publish_date)