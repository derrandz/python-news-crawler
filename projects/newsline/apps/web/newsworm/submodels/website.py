from .abstract_model import AbstractModel
from django.db import models

class Website(AbstractModel):
	name               = models.CharField(max_length=45)
	url                = models.CharField(max_length=255)
	configuration_file = models.CharField(max_length=255)

	@property
	def articles(self):
		"""A website has many Articles"""
		return [crawl.article_set.all() for crawl in self.crawl_set.all()]

	def __str__(self):
		return "name: %s, url: %s" % (self.name, self.url)
	
	def register_crawl(self, sumpath, bfpath):
		return self.crawl_set.create(summary_file=sumpath, bloomfilter_file=bfpath)

	def get_freshest_crawl(self):
		return self.crawl_set.all()[::-1][0]

class WebsiteChild(AbstractModel):
	""" Any child of the website class, be it an article, a configuration, or a file."""
	class Meta:
		abstract = True 

	website = models.ForeignKey(Website, on_delete=models.CASCADE)

class Crawl(WebsiteChild):
	
	summary_file     = models.CharField(max_length=255)
	bloomfilter_file = models.CharField(max_length=255)
	crawl_date       = models.DateTimeField(auto_now=True, blank=True, null=True)

	def save_articles(self, articles):
		for article in articles:
			self.article_set.create(url=article["link"],
									title=article["title"],
									topimage_url=article["topimage_url"],
									authors=article["authors"],
									keywords=article["keywords"],
									publish_date=article["publish_date"],
									content=article["text"],
									crawl=self)

	@property
	def articles(self):
		return self.article_set.all()

	def __str__(self):
		return "summary_file: %s, bloomfilter_file: %s, website: %s" % (self.summary_file, self.bloomfilter_file, self.website.name)