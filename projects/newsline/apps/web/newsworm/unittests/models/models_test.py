from newsline.apps.web.newsworm.submodels.website import Website, ConfigFile, FreshestCrawl
from newsline.apps.web.newsworm.submodels.article import Article

from newsline.functionalities.tests.base_test import BaseTestCase

class WebsiteTestCase(BaseTestCase):

	def testSetUp(self):
		configfile = ConfigFile(path="/test/configfile.conf")
		configfile.save()
		website = Website(name="hespress", url="http://www.google.com", configuration_file=configfile)
		self.print_seperator()
		print("Website url: %s" % website.url)
		print("Website configuration file: %s" % website.configuration_file.path)
		website.save()
		self.print_seperator()
		self.print_success("Creation passed.")

		self.print_seperator()
		self.print_success("Configuration files: %s" % ConfigFile.objects.all())
		self.print_success("Websites: %s" % Website.objects.all())

		self.print_seperator()
		self.print_success("Creation passed.")

class ConfigFileTestCase(BaseTestCase):

	def testSetUp(self):
		configfiles = [
			ConfigFile(path="/test/configfile1.conf"), 
			ConfigFile(path="/test/configfile2.conf"), 
			ConfigFile(path="/test/configfile3.conf")
		]

		for cf in configfiles:
			cf.save()

		self.print_seperator()
		self.print_success("Configuration files: %s" % ConfigFile.objects.all())

class ArticleTestCase(BaseTestCase):

	def testSetUp(self):
		import datetime
		configfile = ConfigFile(path="/test/configfile.conf")
		configfile.save()
		website = Website(name="hespress", url="http://www.hespress.com", configuration_file=configfile)
		website.save()
		article = Article(url="/link/to/article", 
							page="/link/to/page", 
							authors="['author', 'author']", 
							keywords="['key', 'key']", 
							category="/link/to/category",
							website=website, 
							crawl_date=datetime.datetime.now(), publish_date=datetime.datetime.now())

		article.save()

		self.print_success("Articles: %s" % Article.objects.all())
		self.print_seperator()

class FreshestCrawlTestCase(BaseTestCase):

	def testSetUp(self):
		configfile = ConfigFile(path="/test/configfile.conf")
		configfile.save()
		
		website = Website(name="hespress", url="http://www.hespress.com", configuration_file=configfile)
		website.save()

		freshestSummary = FreshestCrawl(crawl_status=True,
										summary_file="/summary_file.json",
										normalized_summary_file="/normalized_summary_file.json",
										bloomfilter_file="/bloomfilter.bin",
										website=website)

		freshestSummary.save()
		self.print_success("freshest summaries: %s" % FreshestCrawl.objects.all())
