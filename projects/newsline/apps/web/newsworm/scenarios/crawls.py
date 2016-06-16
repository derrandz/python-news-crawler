
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
			self.finalize(worm.summarize())

	def finalize(self, summary):
		from newsline.helpers import helpers
		from django.conf import settings

		dirpath = settings.NEWSLINE_DIR +"/apps/web/newsworm/data/%s" % self.website.name
		sumpath = "%s/summary.json" % dirpath
		nsumpath = "%s/normalized_summary.json" % dirpath
		bloomfilterpath = "%s/bloomfilter.bin" % dirpath

		nsummary = normalize(summary)

		helpers.makedir(dirpath)
		
		helpers.write_json("%s" % sumpath, summary)
		helpers.write_json("%s" % nsumpath, nsummary)
		helpers.write_file("%s" % bloomfilterpath, self.bloomfilter(nsummary))

		self.website.register_initial_crawl(sumpath, nsumpath, bloomfilterpath)
		self.extract_articles(nsummary)

	def extract_articles(self, nsummary):
		articles = []
		for article in nsummary:
			articles.append(ArticlesExtractor(article["link"]))

		self.website.save_articles(articles)
		
class CrawlForFreshet:
	pass