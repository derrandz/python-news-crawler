from newsline.apps.web.newsworm.policies.crawls import InitialCrawl
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