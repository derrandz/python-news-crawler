from newsline.apps.web.newsworm.core.worm import Worm, ArticlesExtractor
from newsline.apps.web.newsworm.core.bloom_filter import WormSimpleBloomFilter as BloomFilter
from newsline.apps.web.newsworm.submodels.website import Website, Crawl

class InitialCrawl:
	def __init__(self, website_url, config_file_path=None, custom_summary_path=None):
		self.website = website_url
		self.config_file_path = config_file_path
		self.custom_summary_path = custom_summary_path

	@property
	def website(self):
		return self._website
	
	@website.setter
	def website(self, websiteurl):
		self._website = Website.objects.get(url=websiteurl)

	def parse_config(self):
		from newsline.helpers import helpers
		from django.conf import settings
		if self.config_file_path is not None:
			return helpers.parse_json_file(self.config_file_path)
		else:
			# return helpers.parse_json_file("%s/data/configurations/%s.json" % (settings.NEWSWORM_DIR, self.website.name) )
			return helpers.parse_json_file(self.website.configuration_file )

	def run(self):
		worm = Worm(self.website.url, self.parse_config())

		try:
			worm._launch("smart", force=True)
		except Exception as e:
			print("Crawled failed with %s" % str(e))
			raise e
			# self.handle_exception(e)
		else:
			self.finalize(worm.jsonify())

	def finalize(self, summary):
		from newsline.helpers import helpers
		from django.conf import settings

		date = self.format_date()

		dirpath = "%s/data/crawls/%s" % (settings.NEWSWORM_DIR, self.website.name)
		sumpath = "%s/%s_summary.json" % (dirpath, date)
		bloomfilterpath = "%s/%s_filter.bloom" % (dirpath, date)

		helpers.makedir(dirpath)
		
		helpers.write_json("%s" % sumpath, summary)
		
		nsummary = Worm.normalize_summary(summary)

		self.bloomfilter(nsummary, bloomfilterpath)
		self.extract_articles(self.website.register_crawl(sumpath, bloomfilterpath), nsummary)

	def format_date(self):
		import datetime
		now = datetime.datetime.now()
		return "%d%d_%d_%d_%d" % (now.hour, now.minute, now.month, now.day, now.year)

	def bloomfilter(self, nsummary, path):
		articles = [a["item_url"].encode("utf-8") for a in nsummary]
		mybloomfilter = BloomFilter(len(articles), 0.00001, path)
		mybloomfilter.add(articles)

	def extract_articles(self, crawl, nsummary):
		articles = []
		for article in nsummary:
			articles.append(ArticlesExtractor(self.website.url, article["item_url"])._download())

		crawl.save_articles(articles)

class CrawlForFreshet:
	pass