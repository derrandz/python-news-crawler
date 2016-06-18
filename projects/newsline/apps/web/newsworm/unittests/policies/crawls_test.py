from newsline.apps.web.newsworm.policies.crawls import InitialCrawl
from newsline.apps.web.newsworm.submodels.website import Website
from newsline.functionalities.tests.base_test import BaseTestCase

class InitialCrawlTestCase(BaseTestCase):

	def testSetup(self):
		url = "http://hespress.com"
		website = Website(url=url, name="hespress", configuration_file="%s/data/configurations/hespress.json" % settings.NEWSWORM_DIR)
		from django.conf import settings
		crawl = InitialCrawl(url)