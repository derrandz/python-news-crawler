from newsline.apps.web.newsworm.submodels.policies.crawls import InitialCrawl
from newsline.functionalities.tests.base_test import BaseTestCase

class InitialCrawlTestCase(BaseTestCase):

	def integralTest(self):
		crawl = InitialCrawl("http://hespress.com")