from .abstract_model import AbstractModel
from django.db import models

class ConfigFile(models.Model):
	path = models.CharField(max_length=255)

	def __str__(self):
		return "path: %s" % self.path

class Website(AbstractModel):
	name               = models.CharField(max_length=45)
	url                = models.CharField(max_length=255)
	configuration_file = models.OneToOneField(ConfigFile, on_delete=models.CASCADE, primary_key=True, related_name="configuration_file")

	@property
	def articles(self):
		"""A website has many Articles"""
		return self.articles.all()

	def __str__(self):
		return "name: %s, url: %s" % (self.name, self.url)
		
class WebsiteChild(AbstractModel):
	""" Any child of the website class, be it an article, a configuration, or a file."""
	class Meta:
		abstract = True 

	website = models.ForeignKey(Website, on_delete=models.CASCADE, related_name="%(class)s")

class FreshestCrawl(WebsiteChild):
	
	crawl_status            = models.BooleanField(blank=False, default=False) 
	summary_file            = models.CharField(max_length=255)
	normalized_summary_file = models.CharField(max_length=255)
	bloomfilter_file        = models.CharField(max_length=255)

	def __str__(self):
		return "crawl_status: %s, summary_file: %s, normalized_summary_file: %s, bloomfilter_file: %s, website: %s" % (self.crawl_status, self.summary_file, self.normalized_summary_file, self.bloomfilter_file, self.website.name)