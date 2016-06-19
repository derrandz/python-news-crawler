from newsline.apps.web.newsworm.submodels.website import Website, Crawl
from newsline.apps.web.newsworm.submodels.article import Article

from newsline.functionalities.tests.base_test import BaseTestCase

class WebsiteTestCase(BaseTestCase):

	def testSetUp(self):
		website = Website(name="hespress", url="http://www.google.com", configuration_file="/test/configfile.conf")
		self.print_seperator()
		
		print("Website url: %s" % website.url)
		print("Website configuration file: %s" % website.configuration_file)
		
		website.save()
		
		self.print_seperator()
		self.print_success("Creation passed.")

		self.print_seperator()
		self.print_success("Websites: %s" % Website.objects.all())

		self.print_seperator()
		self.print_success("Creation passed.")

	def testRelations_Crawl(self):
		pass
	
	def testGetFreshetCrawl(self):
		website = Website(name="hespress", url="http://www.google.com", configuration_file="/test/configfile.conf")
		website.save()

		crawl = Crawl(summary_file="/summary1.json", bloomfilter_file="/bloomfilter1.bin", website=website)
		crawl.save()

		crawl = Crawl(summary_file="/summary2.json", bloomfilter_file="/bloomfilter2.bin", website=website)
		crawl.save()

		print(website.get_freshest_crawl())

class ArticleTestCase(BaseTestCase):

	def testSetUp(self):
		import datetime
		website = Website(name="hespress", url="http://www.google.com", configuration_file="/test/configfile.conf")
		website.save()

		crawl = Crawl(summary_file="/summary.json", bloomfilter_file="/bloomfilter.bin", website=website)
		crawl.save()

		article = Article(content = "توالى التهاني والتبريكات على جريدة هسبريس الإلكترونية، بعد تتويجها يوم الأربعاء الماضي بجائزة الصحافة العربية في فئة الصحافة الذكية، وهي الجائزة التي تسلمها المدير العام للمؤسسة، حسان الكنوني، من يد الشيخ مكتوم بن محمد بن راشد، نائب حاكم دبي، في إطار جائزة الصحافة العربية.وفي هذا السياق هنأ اتحاد كتاب المغرب، والتي ينضوي تحتها كتاب وأدباء ومثقفو المغرب، جريدة هسبريس على التتويج الإعلامي الكبير، حيث قال عبد الرحيم العلام، رئيس الاتحاد، إنه يبارك لهسبريس الغراء تتويجها المستحق، وتمنى لها مزيدا من التتويج والتألق والإشعاع\".ويذكر أن الجائزة تمنح لأفضل إنجاز عربي في مجال الصحافة الذكية، متمثلا في تقديم مادة رقمية متميزة صحافياً، من حيث قدرتها على الاستخدام الأمثل للآليات الذكية الجديدة التي توفرها التكنولوجيا، ومساهمتها في إثراء تجربة الجمهور العربي في استخدامه تكنولوجيا المعلومات على مستوى المحتوى والتفاعل.وتم اشتراط العديد من المعايير للفوز بالجائزة الذكية، من بينها \"المهنية\"؛ حيث يجب أن يرتبط الإنجاز بمحتوى صحافي ملتزم بالتقاليد المهنية، التي تتم مراعاتها في الصحافة عموماً، إلى جانب \"ملكية المحتوى\"، وهي أن يقوم الإنجاز على محتوى أسهمت المؤسسة في إنتاجه،فضلا عن معيار \"الانتشار \"",
							url="/link/to/article", authors="['author1', 'author2']", keywords="['keyw1', 'keyw2']", crawl=crawl, publish_date=datetime.datetime.now())

		article.save()

		self.print_success("Articles: %s" % Article.objects.all())

		for a in Article.objects.all():
			self.print_success("Articles content: %s" % a.content)
		self.print_seperator()

class CrawlTestCase(BaseTestCase):
	def _createCrawl(self):
		website = Website(name="hespress", url="http://www.hespress.com", configuration_file="/test/configfile.conf")
		website.save()

		crawl = Crawl(summary_file="/summary_file.json",
								bloomfilter_file="/bloomfilter.bin",
								website=website)

		crawl.save()
		return crawl
	def testSetUp(self):
		self._createCrawl()
		self.print_success("freshest summaries: %s" % Crawl.objects.all())

	def testSaveArticles(self):
		articles = [
			{
				"link": "/link",
				"title": "Some interseting title",
				"topimage_url": "link.jpg",
				"authors": "[Muhammed, Said]",
				"keywords": "[Key1, Key2]",
				"publish_date": "11-22-33",
				"text": "Some text"
			},
			{
				"link": "/link2",
				"title": "Some interseting title2",
				"topimage_url": "link2.jpg",
				"authors": "[Muhammed2, Said2]",
				"keywords": "[Key12, Key22]",
				"publish_date": "11-22-33",
				"text": "Some text2"
			},
			{
				"link": "/link1",
				"title": "Some interseting title1",
				"topimage_url": "link1.jpg",
				"authors": "[Muhammed1, Said1]",
				"keywords": "[Key11, Key21]",
				"publish_date": "11-22-33",
				"text": "Some text1"
			},
		]
		crawl = self._createCrawl()
		crawl.save_articles(articles)

		for a in crawl.article_set.all():
			print("article: %s" % a )
