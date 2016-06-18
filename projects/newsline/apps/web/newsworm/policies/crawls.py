from newsline.apps.web.newsworm.core import worm.Worm, bloom_filter.WormSimpleBloomFilter
from newsline.apps.web.newsworm.submodels.website import Website, Crawl

class InitialCrawl:
	def __init__(self, website_url, config_file_path=None, custom_summary_path=None):
		self.website = website_url
		self.config_file_path = config_file_path
		self.custom_summary_path = custom_summary_path

	def run(self):
		worm = Worm(self.website.url, self.parse_config())

		try:
			worm.launch("smart", force=True)
		except Exception as e:
			self.handle_exception(e)
		else:
			self.finalize(worm.jsonify())

	def finalize(self, summary):
		from newsline.helpers import helpers
		from django.conf import settings

		dirpath = settings.NEWSLINE_DIR +"/apps/web/newsworm/data/%s" % self.website.name
		sumpath = "%s/summary.json" % dirpath
		bloomfilterpath = "%s/bloomfilter.bin" % dirpath

		helpers.makedir(dirpath)
		
		helpers.write_json("%s" % sumpath, summary)
		helpers.write_file("%s" % bloomfilterpath, self.bloomfilter(Worm.normalize(summary), bloomfilterpath))

		self.extract_articles(self.website.register_crawl(sumpath, bloomfilterpath), nsummary):

	def bloomfilter(self, nsummary, path):
		from pybloomfilter import BloomFilter
		articles = [a["item_url"].encode("utf-8") for a in nsummary]
		mybloomfilter = BloomFilter(len(articles), )

	def extract_articles(self, crawl, nsummary):
		articles = []
		for article in nsummary:
			articles.append(ArticlesExtractor(self.website.url, article["url"]))

		crawl.save_articles(articles)


class CrawlForFreshet:
	pass