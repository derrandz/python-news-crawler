from htmldom import htmldom
from django.test import SimpleTestCase
from newsline.apps.web.newsworm.core.worm import Worm, ArticlesExtractor
from newsline.helpers.colors_class import ColorsClass
from newsline.functionalities.tests.base_simple_test import BaseSimpleTestCase
from newsline.apps.web.newsworm.core.regexr import RegexrClass

import re

class WormTestCase(BaseSimpleTestCase):
	'''
	A test suit for the worm class.
	
	Not the best tests in the world, codewise, but they test wsup.
	'''
	def write_to_jsonfile(self, name, results):
		from newsline.helpers import helpers
		from django.conf import settings
		helpers.write_json(settings.NEWSLINE_DIR +"/apps/web/newsworm/unittests/core/_files/_output/%s.json" % name, results)

	def read_from_training_data(self):
		from newsline.helpers import helpers
		from django.conf import settings
		return helpers.parse_json_file(settings.NEWSLINE_DIR +"/apps/web/newsworm/unittests/core/_files/_input/training_set.json")

	def testValidate(self):
		class WormTestClass(Worm):
			def __init__(self, rooturl=None, domitems=None):
				self.regexr = RegexrClass()
				self.rooturl = rooturl
				self.temp = self.validate(domitems)
		

		# 0
		try:
			self.print_info("# 0: The following test should fail.")
			from copy import deepcopy
			worm = WormTestClass("http://www.goud.ma/", 1)
		except Exception as e:
			self.print_failure("# 0: Test failed with :%s"%str(e))
		else:
			self.print_success("# 0: Test passed")


		# 1
		self.print_seperator()
		try:
			self.print_info("# 1: The following test should fail.")
			from copy import deepcopy
			worm = WormTestClass("http://www.goud.ma/", [1, {}])
		except Exception as e:
			self.print_failure("# 1: Test failed with :%s"%str(e))

		else:
			self.print_success("# 1: Test passed")

		# 2
		self.print_seperator()
		try:
			self.print_info("# 2: The following test should pass.")
			from copy import deepcopy
			worm = WormTestClass("http://www.goud.ma/", [{}, {}])
		except Exception as e:
			self.print_failure("# 2: Test failed with :%s"%str(e))

		else:
			self.print_success("# 3: Test passed")


	def testNormalize(self):

		class WormTestClass(Worm):
			def __init__(self, rooturl=None, domitems=None):
				self.regexr = RegexrClass()
				self.rooturl = rooturl

				self.temp = self.normalize(domitems)
		
		domitems = {
			"url": "http://www.goud.ma/", 
			"selector": "", 
			"nested_items":{
				"url": "http://www.goud.ma/topics/1/",
				"selector": "",
				"nested_items": {
					"url": "http://www.goud.ma/topics/2/",
					"selector": "",
					"nested_items":{
						"url": "http://www.goud.ma/topics/3/",
						"selector": ""
					}
				}
			}
		}

		from copy import deepcopy
		worm = WormTestClass("http://www.goud.ma/", deepcopy(domitems))
		self.print_info("'\n\nThe following should contain links with the rooturl as a prefix:")
		self.print_with_color("DARKCYAN", "\n[PreNormaliziation]: %s"% domitems)

		self.print_info("\n\nThe following should contain links without the rooturl as a prefix:")
		self.print_with_color("DARKCYAN", "\n[PostNormalization]: %s"% worm.temp)

	def testDecode(self):

		class WormTestClass(Worm):
			def __init__(self, rooturl=None, domitems=None):
				self.regexr = RegexrClass()
				self.rooturl = rooturl

				self.temp = self.decode(domitems)
		
		domitems = {
			"url": "http://www.goud.ma/", 
			"selector": "", 
			"nested_items":{
				"url": "http://www.goud.ma/topics/%d8%aa%d8%a8%d8%b1%d9%83%d9%8a%d9%83/",
				"selector": "",
				"nested_items": {
					"url": "http://www.goud.ma/topics/%d8%aa%d8%a8%d8%b1%d9%83%d9%8a%d9%83/%d8%aa%d8%a8%d8%b1%d9%83%d9%8a%d9%83/",
					"selector": "",
					"nested_items":{
						"url": "http://www.goud.ma/topics/%d8%aa%d8%a8%d8%b1%d9%83%d9%8a%d9%83/%d8%aa%d8%a8%d8%b1%d9%83%d9%8a%d9%83/%d8%aa%d8%a8%d8%b1%d9%83%d9%8a%d9%83/",
						"selector": ""
					}
				}
			}
		}

		from copy import deepcopy
		worm = WormTestClass("http://www.goud.ma/", deepcopy(domitems))
		self.print_info("'\n\nThe following should contain links with non readable utf-8 characters:")
		self.print_with_color("DARKCYAN", "\n[PreNormaliziation]: %s"% domitems)

		self.print_info("\n\nThe following should contain links with readable arabic unicode characters:")
		self.print_with_color("DARKCYAN", "\n[PostNormalization]: %s"% worm.temp)

	def testClean(self):

		class WormTestClass(Worm):
			def __init__(self, rooturl=None, domitems=None):
				self.regexr = RegexrClass()
				self.rooturl = rooturl

				self.temp = self.clean(domitems)
		
		domitems = {
			"url": "http://www.goud.ma/", 
			"selector": "", 
			"nested_items":{
				"url": "http://www.goud.ma/",
				"selector": "",
				"nested_items": {
					"url": "http://www.goud.ma/topics//1",
					"selector": "",
					"nested_items":{
						"url": "http://www.goud.ma///topics//123//page2/",
						"selector": ""
					}
				}
			}
		}

		from copy import deepcopy
		worm = WormTestClass("http://www.goud.ma/", deepcopy(domitems))
		self.print_info("'\n\nThe following should contain links trailing slashes and double slashes:")
		self.print_with_color("DARKCYAN", "\n[PreNormaliziation]: %s"% domitems)

		self.print_info("\n\nThe following should contain links cleaned from trailing slashes and double slashes:")
		self.print_with_color("DARKCYAN", "\n[PostNormalization]: %s"% worm.temp)

	def testNormalizationPhase(self):

		class WormTestClass(Worm):
			def __init__(self, rooturl=None, domitems=None):
				self.regexr = RegexrClass()
				self.rooturl = rooturl

				self.temp = self.clean(self.decode(self.normalize(self.validate(domitems))))
		
		domitems = {
			"url": "http://www.goud.ma/", 
			"selector": "", 
			"nested_items":{
				"url": "http://www.goud.ma////topics///%d8%aa%d8%a8%d8%b1%d9%83%d9%8a%d9%83/",
				"selector": "",
				"nested_items": {
					"url": "http://www.goud.ma/topics///%d8%aa%d8%a8%d8%b1%d9%83%d9%8a%d9%83/%d8%aa%d8%a8%d8%b1%d9%83%d9%8a%d9%83/",
					"selector": "",
					"nested_items":{
						"url": "http://www.goud.ma///topics///%d8%aa%d8%a8%d8%b1%d9%83%d9%8a%d9%83/%d8%aa%d8%a8%d8%b1%d9%83%d9%8a%d9%83/%d8%aa%d8%a8%d8%b1%d9%83%d9%8a%d9%83/",
						"selector": ""
					}
				}
			}
		}

		from copy import deepcopy
		worm = WormTestClass("http://www.goud.ma/", deepcopy(domitems))
		self.print_info("'\n\nThe following should contain links trailing slashes and double slashes, non-readable utf-8 characters and rooturl prefix:")
		self.print_with_color("DARKCYAN", "\n[PreNormaliziation]: %s"% domitems)

		self.print_info("\n\nThe following should contain links cleaned from trailing slashes and double slashes, readable unicode arabic characters and clean from rooturl prefix:")
		self.print_with_color("DARKCYAN", "\n[PostNormalization]: %s"% worm.temp)

	def testDomItemCreation(self):

		class WormTestClass(Worm):
			def __init__(self, rooturl=None, domitems=None):
				self.regexr = RegexrClass()
				self.rooturl = rooturl

				self.domitems = self.clean(self.decode(self.normalize(self.validate(domitems))))
		
		domitems = {
			"name": "category",
			"url": "/category1/", 
			"selector": "ul > li > a", 
			"nested_items":{
				"name": "article",
				"url": "/category1/article",
				"selector": "h2 > a",
				"nested_items": [
					{
						"name": "article_image",
						"url": "/category1/article/image",
						"selector": "span > img"
					},
					{
						"name": "article_video",
						"url": "/category1/article/video",
						"selector": "span > video"
					}
				]
			}
		}

		from copy import deepcopy
		try:
			worm = WormTestClass("http://www.goud.ma/", deepcopy(domitems))
		except Exception as e:
			self.print_failure("Test failed with error: %s" % str(e))
			raise e
		else:
			self.print_success("Test passed without raising any exception!")
			self.print_success("Testing further more")

			if worm.domitems.name == "category":
				self.print_success("Dom item category has been created successfully with:")
				self.print_with_color("CYAN", "url: %s, domselector: %s" % (worm.domitems.url, worm.domitems.domselector))

				if worm.domitems.has_nested_items:
					self.print_success("Dom item category has nested items:")
					nesteditem = worm.domitems.nested_items

					if nesteditem.name == "article":
						self.print_success("Dom item article has been created successfully with:")
						self.print_with_color("CYAN", "url: %s, domselector: %s" % (nesteditem.url, nesteditem.domselector))

						if nesteditem.has_nested_items:
							self.print_success("Dom item category has nested items:")
							nesteditems = nesteditem.nested_items

							for a in nesteditems:
								if a.name == "article_image":
									self.print_success("Dom item article_image has been created successfully with:")
									self.print_with_color("CYAN", "url: %s, domselector: %s" % (a.url, a.domselector))
								elif a.name == "article_video":
									self.print_success("Dom item article_video has been created successfully with:")
									self.print_with_color("CYAN", "url: %s, domselector: %s" %(a.url, a.domselector))

			self.print_seperator()


	def testPatternize(self):
		class WormTestClass(Worm):
			def __init__(self, rooturl=None, domitems=None):
				self.regexr = RegexrClass()
				self.rooturl = rooturl

				self.domitems = self.clean(self.decode(self.normalize(self.validate(domitems))))
				self.patternize()
		
		catmatches     = ["/category2","/category3","/category4", "/category2/cat", "/category2/categko/123"]
		articlematches = ["/category1/article", "/category1/article", "/category1/article", "/category1/article1", "/category1/article1.php"]
		imgmatches     = ["/category1/article/image", "/category3/article/imageasdas", "/category2/article/image_asd", "/category1/article/image.gp", "/category1/article/image.dp"]
		videomatches   = ["/category1/article/video", "/category3/article1/videoasd", "/category2/article123/videoasd", "/category1/article/videoa21", "/category1/article/video/sdf/kd"]

		domitems = {
			"name": "category",
			"url": "/category1/", 
			"selector": "ul > li > a", 
			"nested_items":{
				"name": "article",
				"url": "/category1/article",
				"selector": "h2 > a",
				"nested_items": [
					{
						"name": "article_image",
						"url": "/category1/article/image",
						"selector": "span > img"
					},
					{
						"name": "article_video",
						"url": "/category1/article/video",
						"selector": "span > video"
					}
				]
			}
		}

		try:
			from copy import deepcopy
			worm = WormTestClass("http://www.goud.ma/", deepcopy(domitems))
		except Exception as e:
			self.print_failure("Test failed with error: %s" % str(e))
			raise e

		else:
			self.print_success("Test passed without raising any exception!")

			if worm.domitems.name == "category":
				self.print_success("Dom item category has been created successfully with:")
				self.print_with_color("CYAN", "url: %s, domselector: %s" % (worm.domitems.url, worm.domitems.domselector))

				for cat in catmatches:
					status = worm.domitems.matches(cat)
					if status is not None:
						if status:
							self.print_success("%s matches %s. OK!" % (cat, worm.domitems.name))
						else:
							self.print_failure("%s does not matche %s. OK!" % (cat, worm.domitems.name))

				if worm.domitems.has_nested_items:
					self.print_success("Dom item category has nested items:")
					nesteditem = worm.domitems.nested_items

					if nesteditem.name == "article":
						self.print_success("Dom item article has been created successfully with:")
						self.print_with_color("CYAN", "url: %s, domselector: %s" % (nesteditem.url, nesteditem.domselector))

						for art in articlematches:
							status = nesteditem.matches(art)
							if status is not None:
								if status:
									self.print_success("%s matches %s. OK!" % (art, nesteditem.name))
								else:
									self.print_failure("%s does not matche %s. OK!" % (art, nesteditem.name))

						if nesteditem.has_nested_items:
							self.print_success("Dom item category has nested items:")
							nesteditems = nesteditem.nested_items

							for a in nesteditems:
								if a.name == "article_image":
									self.print_success("Dom item article_image has been created successfully with:")
									self.print_with_color("CYAN", "url: %s, domselector: %s" % (a.url, a.domselector))
									for img in imgmatches:
										status = nesteditem.matches(img)
										if status is not None:
											if status:
												self.print_success("%s matches %s. OK!" % (img, nesteditem.name))
											else:
												self.print_failure("%s does not matche %s. OK!" % (img, nesteditem.name))
								elif a.name == "article_video":
									self.print_success("Dom item article_video has been created successfully with:")
									self.print_with_color("CYAN", "url: %s, domselector: %s" %(a.url, a.domselector))
									for vid in videomatches:
										status = nesteditem.matches(vid)
										if status is not None:
											if status:
												self.print_success("%s matches %s. OK!" % (vid, nesteditem.name))
											else:
												self.print_failure("%s does not matche %s. OK!" % (vid, nesteditem.name))

			self.print_seperator()

	def testExtract(self):
		domitems = {
			"name": "category",
			"url": "/politique/index.1.html", 
			"selector": "div#mainNav > ul#menu_main > li > a", 
		}

		try:
			from copy import deepcopy
			worm = Worm("http://www.hespress.com/", deepcopy(domitems))
		except Exception as e:
			self.print_failure("Test failed with error: %s" % str(e))
			raise e
		else:
			self.print_success("Extracted data:\n %s" % worm._extract(domitems["url"]))

	def testCrawl(self):
		domitems = {
			"name": "category",
			"url": "/politique/index.1.html", 
			"selector": "div#mainNav > ul#menu_main > li > a", 
		}

		try:
			from copy import deepcopy
			worm = Worm("http://www.hespress.com/", deepcopy(domitems))
		except Exception as e:
			self.print_failure("Test failed with error: %s" % str(e))
			raise e
		else:
			self.print_success("Extracted data:\n %s" % worm._crawl(worm.domitems))

	def testCrawlHyperLinks(self):
		domitems = {
			"name": "category",
			"url": "/politique/index.1.html", 
			"selector": "div#mainNav > ul#menu_main > li > a", 
		}

		try:
			from copy import deepcopy
			worm = Worm("http://www.hespress.com/", deepcopy(domitems))
		except Exception as e:
			self.print_failure("Test failed with error: %s" % str(e))
			raise e
		else:
			self.print_success("Extracted data:\n %s" % worm._crawl_hyperlinks(worm.domitems))

	def testCrawlHyperLinks(self):
		domitems = {
			"name": "category",
			"url": "/politique/index.1.html", 
			"selector": "div#mainNav > ul#menu_main > li > a", 
		}

		try:
			from copy import deepcopy
			worm = Worm("http://www.hespress.com/", deepcopy(domitems))
		except Exception as e:
			self.print_failure("Test failed with error: %s" % str(e))
			raise e
		else:
			self.print_success("Extracted data:\n %s" % worm._crawl_similar_hyperlinks(worm.domitems, ""))

		self.print_seperator()

		domitems = {
			"name": "article",
			"url": "/politique/304866.html", 
			"selector": "h2.section_title > a", 
		}

		try:
			from copy import deepcopy
			worm = Worm("http://www.hespress.com/", deepcopy(domitems))
		except Exception as e:
			self.print_failure("Test failed with error: %s" % str(e))
			raise e
		else:
			self.print_success("Extracted data:\n %s" % worm._crawl_similar_hyperlinks(worm.domitems, "/politique"))

	def testPipeout(self):
		domitems = {
			"name": "category",
			"url": "/politique/index.1.html", 
			"selector": "div#mainNav > ul#menu_main > li > a", 
		}

		try:
			from copy import deepcopy
			worm = Worm("http://www.hespress.com/", deepcopy(domitems))
		except Exception as e:
			self.print_failure("Test failed with error: %s" % str(e))
			raise e
		else:
			self.print_success("Extracted data:\n %s" % worm._pipeout(worm.domitems, ""))

	def testPipeoutToCrawledItem(self):
		domitems = {
			"name": 'category',
			"url": '/politique/index.1.html', 
			"selector": 'div#mainNav > ul#menu_main > li > a',
			"nested_items":{
				"name": 'article',
				"url": '/politique/212121.html',
				"selector": 'h2.section_title > a'	
			} 
		}

		try:
			from copy import deepcopy
			worm = Worm("http://www.hespress.com/", deepcopy(domitems))
		except Exception as e:
			self.print_failure("Test failed with error: %s" % str(e))
			raise e
		else:
			crawled_items = worm._pipeout(worm.domitems, "")
			worm.domitems.crawled_items = crawled_items
			self.print_success("----------------- Piped out : %s" % worm.domitems.crawled_items)

			self.print_info("----------------- Crawling subitems")
			for i in worm.domitems.crawled_items:
				self.print_success("----------------- Crawling: %s" % i.url)
				self.print_success("----------------- Respective DomItem: %s" % i.dom_item.name)
				worm._pipeout_to_crawled_item(i, 'smart')
				self.print_success("Extracted data:%s\n" % i.nested_items)

	def testLaunch(self):
		domitems = {
			"name": 'category',
			"url": '/politique/index.1.html', 
			"selector": 'div#mainNav > ul#menu_main > li > a',
			"nested_items":{
				"name": 'article',
				"url": '/politique/212121.html',
				"selector": 'h2.section_title > a'	
			} 
		}

		try:
			from copy import deepcopy
			worm = Worm("http://www.hespress.com/", deepcopy(domitems))
		except Exception as e:
			self.print_failure("Test failed with error: %s" % str(e))
			raise e
		else:
			worm._launch()
			self.print_info("----------------- Crawling finished.")
			def _pt(crawleditem):
				print("[%s]Crawled item: %s" % (crawleditem.dom_item.name, crawleditem.url))

			for ci in worm.domitems.crawled_items:
				ci.diverge(_pt)

	def testSummary(self):
		domitems = {
			"name": 'category',
			"url": '/politique/index.1.html', 
			"selector": 'div#mainNav > ul#menu_main > li > a',
			"nested_items":{
				"name": 'article',
				"url": '/politique/212121.html',
				"selector": 'h2.section_title > a'	
			} 
		}

		try:
			from copy import deepcopy
			worm = Worm("http://www.hespress.com/", deepcopy(domitems))
		except Exception as e:
			self.print_failure("Test failed with error: %s" % str(e))
			raise e
		else:
			worm._launch()
			self.print_info("----------------- Crawling finished.")
			self.write_to_jsonfile("testSummary_jsonfile", worm._summary())

	def testSummaryMultipage(self):
		rooturl = "http://www.hespress.com/"
		domitems = {
			"name": 'category',
			"url": '/politique/index.1.html', 
			"selector": 'div#mainNav > ul#menu_main > li > a',
			"nested_items":{
				"name": 'page',
				"url": '/politique/index.2.html',
				"selector": 'div#box_pagination > span.pagination > a',
				"nested_items":{
					"name": 'article',
					"url": '/politique/212121.html',
					"selector": 'h2.section_title > a'
				}	
			} 
		}

		# rooturl = "http://www.goud.ma"
		# domitems = {
		# 	"name": 'category',
		# 	"url": r'http://www.goud.ma/topics/آش-واقع',  
		# 	"selector": 'ul.main-menu > li.menu-item > a',
		# 	"nested_items":{
		# 		"name": 'page',
		# 		"url": r'http://www.goud.ma/topics/%d8%aa%d8%a8%d8%b1%d9%83%d9%8a%d9%83/page/2/',
		# 		"selector": 'div.pagination > a',
		# 		"nested_items":{
		# 			"name": 'article',
		# 			"url": r'http://www.goud.ma/%D8%B5%D8%A7%D9%81%D9%8A%D9%86%D8%A7%D8%B2-%D9%82%D8%B6%D9%8A%D8%A9-%D9%8A%D9%87%D9%88%D8%AF%D9%8A%D8%A9-%D9%87%D8%B1%D8%A8%D8%AA-%D9%85%D9%86-%D8%AA%D8%AC%D8%A7%D8%B1%D8%A9-%D8%A7%D9%84%D8%AC%D9%86-220161/',
		# 			"selector": 'h2 > a'
		# 		}	
		# 	}
		# }

		try:
			from copy import deepcopy
			worm = Worm(rooturl, deepcopy(domitems))
			worm._launch("smart")
		except Exception as e:
			self.print_failure("Test failed with error: %s" % str(e))
			raise e
		else:
			self.print_info("----------------- Crawling finished.")
			self.write_to_jsonfile("testSummaryMultipage_jsonfile", worm._summary())

	def testJsonify(self):
		domitems = {
			"name": 'category',
			"url": '/politique/index.1.html', 
			"selector": 'div#mainNav > ul#menu_main > li > a',
			"nested_items":{
				"name": 'article',
				"url": '/politique/212121.html',
				"selector": 'h2.section_title > a'	
			} 
		}

		try:
			from copy import deepcopy
			worm = Worm("http://www.hespress.com/", deepcopy(domitems))
		except Exception as e:
			self.print_failure("Test failed with error: %s" % str(e))
			raise e
		else:
			worm._launch()
			self.print_info("----------------- Crawling finished.")
			self.write_to_jsonfile("testJsonify.json", worm.jsonify())

	def testJsonifyMultipage(self):
		rooturl = "http://www.hespress.com/"
		domitems = {
			"name": 'category',
			"url": '/politique/index.1.html', 
			"selector": 'div#mainNav > ul#menu_main > li > a',
			"nested_items":{
				"name": 'page',
				"url": '/politique/index.2.html',
				"selector": 'div#box_pagination > span.pagination > a',
				"nested_items":{
					"name": 'article',
					"url": '/politique/212121.html',
					"selector": 'h2.section_title > a'
				}	
			} 
		}

		# rooturl = "http://www.goud.ma"
		# domitems = {
		# 	"name": 'category',
		# 	"url": r'http://www.goud.ma/topics/آش-واقع',  
		# 	"selector": 'ul.main-menu > li.menu-item > a',
		# 	"nested_items":{
		# 		"name": 'page',
		# 		"url": r'http://www.goud.ma/topics/%d8%aa%d8%a8%d8%b1%d9%83%d9%8a%d9%83/page/2/',
		# 		"selector": 'div.pagination > a',
		# 		"nested_items":{
		# 			"name": 'article',
		# 			"url": r'http://www.goud.ma/%D8%B5%D8%A7%D9%81%D9%8A%D9%86%D8%A7%D8%B2-%D9%82%D8%B6%D9%8A%D8%A9-%D9%8A%D9%87%D9%88%D8%AF%D9%8A%D8%A9-%D9%87%D8%B1%D8%A8%D8%AA-%D9%85%D9%86-%D8%AA%D8%AC%D8%A7%D8%B1%D8%A9-%D8%A7%D9%84%D8%AC%D9%86-220161/',
		# 			"selector": 'h2 > a'
		# 		}	
		# 	}
		# }

		try:
			from copy import deepcopy
			worm = Worm(rooturl, deepcopy(domitems))
			worm._launch("smart")
		except Exception as e:
			self.print_failure("Test failed with error: %s" % str(e))
			raise e
		else:
			self.print_info("----------------- Crawling finished.")
			self.write_to_jsonfile("testJsonfiyMultipage.json", worm.jsonify())

	def crawledItemSetUpTest(self):
		from newsline.apps.web.newsworm.core.worm import CrawledItem
		from newsline.apps.web.newsworm.core.worm import WDomItem
		name = "an item's name"
		url = "http://www.google.com"
		selector = "div.class > ul#id > li > a"
		domitem_1 = WDomItem(name + "1", url, selector + "1")
		domitem_2 = WDomItem(name + "2", url, selector + "2")
		domitem_3 = WDomItem(name + "3", url, selector + "3")

		try:
			self.print_info("Setting up a crawled item with no nested crawled items")
			crawleditem = CrawledItem("link", domitem_1)
		except Exception as e:
			self.print_failure("Test failed with error: %s" % str(e))
			raise e
		else:
			self.print_success("Successfuly sat up a crawled item with no nested crawled items")
			self.print_success("Crawled item: %s" % str(crawleditem))
			self.print_success("Crawled item's dom item: %s" % str(crawleditem.dom_item))

		self.print_seperator()

		try:
			self.print_info("Setting up a crawled item with one nested crawled items")
			crawleditem = CrawledItem("A link", domitem_1, CrawledItem("A sublink", domitem_2))
		except Exception as e:
			self.print_failure("Test failed with error: %s" % str(e))
			raise e
		else:
			self.print_success("Successfuly sat up a crawled item with one nested crawled items")

		self.print_seperator()
		
		try:
			self.print_info("Setting up a crawled item with a list nested crawled items")
			crawleditem = CrawledItem("A link", domitem_1, [
				CrawledItem("A sublink", domitem_2), 
				CrawledItem("A sublink", domitem_2)
			])

		except Exception as e:
			self.print_failure("Test failed with error: %s" % str(e))
			raise e
		else:
			self.print_success("Successfuly sat up a crawled item with a list nested crawled items")

		self.print_seperator()
		
		try:
			self.print_info("Setting up a crawled item with a list of nested crawled items that also have one nested item each")
			crawleditem = CrawledItem("A link", domitem_1, [
				CrawledItem("A sublink", domitem_2, 
					CrawledItem("An image", domitem_3, CrawledItem("An image", domitem_3))
				), 
				CrawledItem("A sublink", domitem_2,
					CrawledItem("An image", domitem_3, CrawledItem("An image", domitem_3))
				)
			])
		except Exception as e:
			self.print_failure("Test failed with error: %s" % str(e))
			raise e
		else:
			self.print_success("Successfuly sat up a crawled item with a list of nested crawled items that also have one nested item each")

		self.print_seperator()
		
		try:
			self.print_info("Setting up  a crawled item with a list of nested crawled items that also have a list of nested items each")
			crawleditem = CrawledItem("A link", domitem_1, [
				CrawledItem("A sublink", domitem_2, [
					CrawledItem("An image", domitem_3, CrawledItem("An image", domitem_3)),
					CrawledItem("An image", domitem_3, CrawledItem("An image", domitem_3))
				]), 
				CrawledItem("A sublink", domitem_2, [
					CrawledItem("An image", domitem_3, CrawledItem("An image", domitem_3)),
					CrawledItem("An image", domitem_3, CrawledItem("An image", domitem_3))
				])
			])
		except Exception as e:
			self.print_failure("Test failed with error: %s" % str(e))
			raise e
		else:
			self.print_success("Successfuly sat up a crawled item with a list of nested crawled items that also have a list of nested items each")

		try:
			self.print_info("Setting up a crawled item and then appending a nested item")
			crawleditem = CrawledItem("A link", domitem_1)
			crawleditem.nested_items.append(CrawledItem("A Sublink", domitem_1))
		except Exception as e:
			self.print_exception(e)
			raise e
		else:
			self.print_success("Successfuly sat up a crawled item with a list of nested crawled items that also have a list of nested items each")

	def testWDomItemSetUp(self):
		from newsline.apps.web.newsworm.core.worm import WDomItem, CrawledItem
		""" 
			This method wil ltest the insertion of the crawled data only.
			As of the instantiation of DomItem, it has been tested in dom_item_test
		"""

		try:
			domitem_with_crawled_data = WDomItem(
				"a name",
				"http://www.google.com", 
				"ul > li > a", 
				nested_items=None, 
				crawled_items=CrawledItem("An Image"))
		except Exception as e:
			self.print_exception(e)
			raise e
		else:
			self.print_success("Test succeeded")
			self.print_success("DomItem %s" % str(domitem_with_crawled_data))
			self.print_success("Crawled item printed from the DomItem's attribute %s" % domitem_with_crawled_data.crawled_items)

		self.print_seperator()
		self.print_seperator()

		try:
			domitem_with_crawled_data = WDomItem(
				"a name",
				"http://www.google.com", 
				"ul > li > a", 
				nested_items=None, 
				crawled_items=[
					CrawledItem("An Image"), 
					CrawledItem("Another Image")
				])
		except Exception as e:
			self.print_exception(e)
			raise e
		else:
			self.print_success("Test succeeded")
			self.print_success("DomItem %s" % str(domitem_with_crawled_data))

			for i in domitem_with_crawled_data.crawled_items:
				self.print_success("CrawledItem: %s\n" % i.url)

	def testIntegralCrawl(self):

		from newsline.helpers import helpers
		from django.conf import settings
		training_data = helpers.parse_json_file(settings.NEWSLINE_DIR +"/apps/web/newsworm/unittests/core/_files/_input/training_data.json")

		for name, website in training_data.items():
			if name != "assdae":
				continue
			
			print("Crawling %s" % name)
			try:
				from copy import deepcopy
				worm = Worm(website["root_url"], deepcopy(website["domitems"]))
			except Exception as e:
				self.print_failure("----------------- Crawling failed for [%s] with errors: %s" % (name, str(e)))
				raise e
			else:
				from requests.exceptions import RequestException
				try:
					worm._launch("smart", force=True)
				except RequestException as e:    # This is the correct syntax
					self.print_failure("-----------------  Crawling halted for . [%s] with :%s" % (name, e))
					summary = worm._summary()
					summary["status"] = e
					helpers.write_json(settings.NEWSLINE_DIR +"/apps/web/newsworm/unittests/core/_files/_input/training_data.json", summary)
				else:
					self.print_info("-----------------  Crawling finished successfully for %s " % name)
					self.write_to_jsonfile(name, worm.jsonify())

					website["status"] = "done"
					from newsline.helpers import helpers
					from django.conf import settings
					helpers.write_json(settings.NEWSLINE_DIR +"/apps/web/newsworm/unittests/core/_files/_input/training_data.json", training_data)

		self.print_success("Done.")
		self.print_seperator()


	def verify_crawled(self):
		training_set = self.read_from_training_data() 
		from newsline.helpers import helpers
		from django.conf import settings
		training_data = helpers.parse_json_file(settings.NEWSLINE_DIR +"/apps/web/newsworm/unittests/core/_files/_input/training_data.json")

		for name, website in training_data.items():
			if name in training_set:
				self.print_success("%s passed" % name)
			else:
				self.print_failure("%s did not pass" % name)

	def get_articles(self):
		import newspaper
		from newsline.helpers import helpers
		from django.conf import settings
		sitemap = helpers.parse_json_file(settings.NEWSLINE_DIR +"/apps/web/newsworm/unittests/core/_files/_output/assdae.json")

		def crawl(dictel):
			if 'type' in dictel:
				if dictel['type'] == 'page':
					for key, val in dictel['nested_items'].items():
						a = newspaper.Article("http://assdae.com/" + key, language='ar')
						a.download()
						if a.is_downloaded:
							a.parse()
							a.nlp()
						else:
							a.text = 'Failed to download'	

						content = "link: %s\n" % key

						content += "\n\ntitle: %s" % a.title if a.title else "\n\ntitle:[]"
						content += "\n\ntopimage_url: %s" % a.top_image if a.top_image else "\n\ntopimage_url:[]"
						content += "\n\npublish_date: %s" % a.publish_date.strftime('%m/%d/%Y') if a.publish_date else "\n\npublish_date:[]"
						content +=  "\n\nauthors: %s" % a.authors if a.authors else "\n\nauthors:[]"
						content +=   "\n\nkeywords: %s" % a.keywords if a.keywords else "\n\nkeywords:[]"
						content +=   "\n\ntext: %s" % a.text if a.text else "\n\ntext:[]"

						helpers.file_put_contents(settings.NEWSLINE_DIR +"/apps/web/newsworm/unittests/core/_files/_output/assdae/%s.txt" % key.replace('/', '_'), content)
						print("%s" % key)
		
		helpers.walk_dictionary(sitemap, crawl)

	def testAutoGenDI(self):
		domitems = {
			"name": 'category',
			"url": '/politique/index.1.html', 
			"selector": 'div#mainNav > ul#menu_main > li > a',
			"nested_items":{
				"name": 'page',
				"url": '/politique/index.%d.html',
				"autogen": True,
				"range": [0, 20],
				# "parentless": True,
				"nested_items":{
					"name": 'article',
					"url": '/politique/212121.html',
					"selector": 'h2.section_title > a'
				}	
			} 
		}

		
		class AutoGenWorm(Worm):
			def __init__(self, rooturl=None, domitems=None):
				self.regexr = RegexrClass([]) # Explicitly passing an empty list to indicate that this instance will be used as a helper only.
				self.rooturl = rooturl

				# This is called the normalization phase
				# The nesting of the function calls is very important
				self.domitems = self.clean(self.decode(self.normalize(self.validate(domitems))))

		try:
			worm = AutoGenWorm("http://hespress.com", domitems)
		except Exception as e:
			self.print_exception(e)
			raise e
		else:
			self.print_success("Test passed!")
			self.print_info("%s" % worm.domitems.nested_items[0])

	def testCrawlWithAutoGen(self):
		# rooturl = "http://www.andaluspress.com/"
		# domitems = {
		# 		"name": "category",
		# 		"selector": "div.mynav > ul > li > a",
		# 		"url": "/news/?cat=politique",
		# 		"nested_items": {
		# 			"name": "page",
		# 			"selector": "ul.pagination > li > a",
		# 			"url": "/news/?cat=politique&page=%d",
		# 			"nested_items": {
		# 				"name": "article",
		# 				"selector": "div.cd-resultNw > a",
		# 				"url": "/info-article/?id=933&t=\u0627\u0644\u0645\u0644\u0643-\u0645\u062d\u0645\u062f-\u0627\u0644\u0633\u0627\u062f\u0633-\u064a\u062c\u0631\u064a-\u0628\u0628\u0643\u064a\u0646-\u0645\u0628\u0627\u062d\u062b\u0627\u062a-\u0645\u0639-\u0627\u0644\u0631\u0626\u064a\u0633-\u0634\u064a-\u062c\u064a\u0646-\u0628\u064a\u0646\u063a"
		# 			}
		# 		}
		# 	}

		rooturl = "http://www.hespress.com/"
		domitems = {
			"name": "category",
			"url": "/politique/index.1.html",
			"selector": "div#mainNav > ul#menu_main > li > a",
			"nested_items": {
				"name": "page",
				"selector": "div#box_pagination > span.pagination > a",
				"url": "/politique/index.%d.html",
				"autogen": "True",
				"range": [0, 2],
				"nested_items": {
					"name": "article",
					"selector": "h2.section_title > a",
					"url": "/politique/212121.html"
				},
			},
		}

		# rooturl = "http://telexpresse.com"
		# domitems = {
		# 	"name": "category",
		# 	"url": "category/مجتمع/4/تصنيفات.html",
		# 	"selector": "div.menusprites > ul > li > a",
		# 	"nested_items": {
		# 		"name": "page",
		# 		"selector": "div#box_pagination > span.pagination > a",
		# 		"url": "category/مجتمع/4/%d/تصنيفات.html",
		# 		"autogen": True,
		# 		"range": [0, 5],
		# 		"nested_items": {
		# 			"name": "article",
		# 			"selector": "center > a",
		# 			"url": "تلكسبريس/اخبار سياسية/53045/هافينغتون بوست وفاة زعيم البوليساريو فرصة لوضع حد لأحد أكثر النزاعات سخافة في العالم.html"
		# 		}
		# 	}
		# }

		try:
			worm = Worm(rooturl, domitems)
		except Exception as e:
			self.print_failure("----------------- Crawling failed with errors: %s" % (str(e)))
			raise e
		else:
			from requests.exceptions import RequestException
			try:
				worm._launch("smart", force=True)
			except RequestException as e:    # This is the correct syntax
				self.print_failure("-----------------  Crawling halted for . [%s] with :%s \n %s" % (name, e, worm._summary()))
			else:
				self.print_info("-----------------  Crawling finished successfully for andaluspress ")
				self.write_to_jsonfile("testAutogen", worm.jsonify())

	def testJsonNormalization(self):
		from newsline.helpers import helpers
		from django.conf import settings
		summary = helpers.parse_json_file(settings.NEWSLINE_DIR +"/apps/web/newsworm/unittests/core/_files/_output/akhbarona.json")

		print(Worm.normalize(summary))

class ArticleExtractorTestCase(BaseSimpleTestCase):

	def testSetUp(self):
		article = ArticlesExtractor("http://www.hespress.com", "/politique/308315.html")._download()

		for key, val in article.items(): 
			print("%s: %s" % (key, val))