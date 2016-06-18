from .abstract_model import AbstractModel
from django.db import models

class ConfigFile(models.Model):
	path = models.CharField(max_length=255)

	def __str__(self):
		return "path: %s" % self.path

class Website(AbstractModel):
	name               = models.CharField(max_length=45)
	url                = models.CharField(max_length=255)
	configuration_file = models.OneToOneField(ConfigFile, primary_key=True, on_delete=models.CASCADE, related_name="configuration_file")

	@property
	def articles(self):
		"""A website has many Articles"""
		return self.article_set.all()

	def __str__(self):
		return "name: %s, url: %s" % (self.name, self.url)
	
	def register_crawl(self, sumpath, bfpath):
		return self.crawl_set.create(Crawl(summary_file=sumpath, bloomfilter_file=bfpath))


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


	def __str__(self):
		return "summary_file: %s, bloomfilter_file: %s, website: %s" % (self.summary_file, self.bloomfilter_file, self.website.name)