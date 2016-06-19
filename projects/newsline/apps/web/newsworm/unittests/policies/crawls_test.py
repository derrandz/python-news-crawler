from newsline.apps.web.newsworm.policies.crawls import InitialCrawl, CrawlForFreshest
from newsline.apps.web.newsworm.submodels.website import Website
from newsline.functionalities.tests.base_test import BaseTestCase

class InitialCrawlTestCase(BaseTestCase):

	def testSetUp(self):
		from django.conf import settings
		url = "http://hespress.com"
		website = Website(url=url, name="hespress", configuration_file="%s/data/configurations/hespress.json" % settings.NEWSWORM_DIR)
		website.save()

		crawl = InitialCrawl(url)

		if crawl.website == website:
			self.print_success("Test passed")
		else:
			self.print_failure("Test failed")

	def testRun(self):
		from django.conf import settings
		url = "http://hespress.com"
		website = Website(url=url, name="hespress", configuration_file="%s/data/configurations/hespress.json" % settings.NEWSWORM_DIR)
		website.save()

		crawl = InitialCrawl(url)

		crawl.run()

		print(website.articles)

class CrawlForFreshestTestCase(BaseTestCase):

	def testSetUp(self):
		from django.conf import settings
		url = "http://hespress.com"
		website = Website(url=url, name="hespress", configuration_file="%s/data/configurations/hespress.json" % settings.NEWSWORM_DIR)
		website1 = Website(url="https://telexpress.com", name="telexpress", configuration_file="%s/data/configurations/hespress.json" % settings.NEWSWORM_DIR)
		website.save()
		website1.save()

		crawl = CrawlForFreshest(url)

		if crawl.website == website:
			self.print_success("Test passed")
		else:
			self.print_failure("Test failed")

	def testRun(self):
		from django.conf import settings
		url = "http://hespress.com"
		website = Website(url=url, name="hespress", configuration_file="%s/data/configurations/hespress.json" % settings.NEWSWORM_DIR)
		website.save()

		website.register_crawl("344_6_18_2016_summary.json", "344_6_18_2016_filter.bloom")
		website.register_crawl("355_6_18_2016_summary.json", "355_6_18_2016_filter.bloom")
		website.register_crawl("416_6_18_2016_summary.json", "416_6_18_2016_filter.bloom")

		crawl = CrawlForFreshest(url)

		crawl.run()
		if len(website.crawl_set.all()) > 4:
			self.print_success("Apprently we have a new crawl added!")
			freshest_crawl = website.get_freshest_crawl()
			if freshest_crawl:
				for article in freshest_crawl.articles:
					print("Fresh links %s" % article.url)
