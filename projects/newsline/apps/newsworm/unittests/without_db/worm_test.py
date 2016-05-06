import re

from htmldom import htmldom
from newsline.apps.newsworm.core.worm import Worm
from django.test import SimpleTestCase
from .base_test import BaseSimpleTestCase, ColorsClass
from newsline.apps.newsworm.core.regexr import RegexrClass

class WormTestCase(BaseSimpleTestCase):
	'''
	A test suit for the worm class.
	
	Not the best tests in the world, codewise, but they test wsup.
	'''
	def test_hespress(self):
		self.test_worm_regexr({"root_url":"http://www.hespress.com", "url_example": ["/politique.index.1.html", "/art-et-culture/index.1.html"], "dom_path": "ul[id=menu_main] > li > a"})
	
	def test_alyaoum(self):
		self.test_worm_regexr({"root_url":"http://www.alyaoum24.com", "url_example": ["http://www.alyaoum24.com/news/sport", "http://www.alyaoum24.com/news/women"], "dom_path": "ul[id~=menu-mainmenu] > li[class~=menu-item] > a"})

	def test_other(self):
		self.test_worm_regexr({"root_url":"http://www.lefigaro.fr", "url_example": ["http://www.lefigaro.fr/economie", "http://www.lefigaro.fr/culture"], "dom_path": "ul[class~=figh-keyword__list] > li[class~=figh-keyword__item] > a[class~=figh-keyword__link]"})

	def test_hespress_all(self):
		self.test_worm_regexr_articles({"root_url":"http://www.hespress.com", 
										"url_example": ["/politique.index.1.html", "/art-et-culture/index.1.html"], 
										"article_example": ["/politique/304713.html", "/art-et-culture/304866.html"], 
										"cat_dom_path": "ul[id=menu_main] > li > a",
										"art_dom_path": "h2[class~=section_title] > a"})

	def test_kifach_all(self):
		self.test_worm_regexr_articles({"root_url":"http://www.kifache.com", 
										"url_example": ["http://www.kifache.com/category/sdlfsdd"], 
										"article_example": ["http://www.kifache.com/90353"], 
										"cat_dom_path": "div[id=mainmenu] > ul > li > a",
										"art_dom_path": "h2 > a"})

	def test_goud_all(self):
		self.test_worm_regexr_articles({"root_url":"http://www.kifache.com", 
										"url_example": ["http://www.kifache.com/category/sdlfsdd"], 
										"article_example": ["http://www.kifache.com/90353"], 
										"cat_dom_path": "div[id=mainmenu] > ul > li > a",
										"art_dom_path": "h2 > a"})

	def test_goud_all(self):
		self.test_worm_regexr_articles({"root_url":"http://www.goud.ma", 
										"url_example": ["http://www.goud.ma/topics/%d8%aa%d8%a8%d8%b1%d9%83%d9%8a%d9%83/"], 
										"article_example": ["http://www.goud.ma/%d9%88%d8%a7%d8%b4-%d8%a8%d8%b5%d8%a7%d8%ad-%d8%a7%d9%84%d9%88%d8%b2%d9%8a%d8%b1-%d8%ad%d9%81%d9%8a%d8%b8-%d8%a7%d9%84%d8%b9%d9%84%d9%85%d9%8a-%d9%87%d8%af%d8%af-%d8%b5%d8%ad%d8%a7%d9%81%d9%8a%d8%a9-216605/"], 
										"cat_dom_path": "a",
										"art_dom_path": "a"})

	def test_worm_regexr_articles(self, details):
		regxr = RegexrClass()

		cat_url_example = []
		for u in details["url_example"]:
			cat_url_example.append(regxr.del_substring(details["root_url"], u))
	
		art_url_example = []
		for u in details["article_example"]:
			art_url_example.append(regxr.del_substring(details["root_url"], u))

		cat_dom_path = details["cat_dom_path"]
		art_dom_path = details["art_dom_path"]

		worm = Worm(details["root_url"], {
												"category_url": cat_url_example, 
												"category_dom_path": cat_dom_path, 
												"category_article_url": art_url_example,
												"article_dom_path": art_dom_path
												}
					)

		cdom_mainmenu = htmldom.HtmlDom(worm.root_url).createDom().find(worm.category["category_dom_path"])

		# The url we ought to match
		regxr = RegexrClass() 
		test_urls = []
		for a in cdom_mainmenu:
			test_urls.append(regxr.del_substring(worm.root_url, a.attr("href")))

		regex = worm.patternize_url_category()

		# The extracted regex pattern
		self.print_with_color("YELLOW","\n\nThe extracted regex pattern is: %s" % regex[0])

		print("\n\nThe provided url example:")
		if len(cat_url_example) > 1:
			for url in cat_url_example:
				self.print_with_color("GREEN", "%s\n" % url)
		else:
			self.print_with_color("GREEN", "%s\n" % cat_url_example[0])

		print("We will try to match against [Categories]:\n")
		for u in test_urls :
			self.print_with_color("GREEN",ColorsClass.UNDERLINE + "%s " % u )

		successes = 0
		failures  = 0
		s_cat_urls = []
		# Should match against urls
		for u in test_urls:
			self.print_info("\nMatching for %s ..." % u)
			res = regex[1].match(u)
			if res:
				self.print_success("Match success!: ")
				s_cat_urls.append(u)
				successes += 1
				print("\n")
			else:
				self.print_failure("Match failed.")
				failures += 1

		self.print_with_bold_color("BLUE", "\n\nTest done with : success : %d  |  failures : %d" % (successes, failures))

		
		for u in s_cat_urls:
			print("Category: %s" % u)
			cdom_mainmenu = htmldom.HtmlDom(worm.root_url + u).createDom().find(worm.category["article_dom_path"])

			a_success = 0
			a_failure = 0
			crawled_urls = []
			for a in cdom_mainmenu:
				crawled_urls.append(regxr.del_substring(worm.root_url, a.attr("href")))

			regex = worm.patternize_url_article()

			for u in crawled_urls:
				self.print_info("\nMatching for %s ..." % u)
				res = regex[1].match(u)
				if res:
					self.print_success("Match success!: ")
					a_success += 1
					print("\n")
				else:
					self.print_failure("Match failed.")
					a_failure += 1
			self.print_with_bold_color("BLUE", "\n\nTest done with for cat = %s : success : %d  |  failures : %d" % (u, a_success, a_failure))


	def test_worm_regexr(self, details):
		regxr = RegexrClass()

		url_example = []
		for u in details["url_example"]:
			url_example.append(regxr.del_substring(details["root_url"], u))
		

		dom_path = details["dom_path"]

		worm = Worm(details["root_url"], {
												"category_url": url_example, 
												"category_dom_path": dom_path, 
												"category_article_url": ""
												}
					)

		cdom_mainmenu = htmldom.HtmlDom(worm.root_url).createDom().find(worm.category["dom_path"])

		# The url we ought to match 
		test_urls = []
		for a in cdom_mainmenu:
			test_urls.append(regxr.del_substring(worm.root_url, a.attr("href")))

		regex = worm.patternize_url_category()

		# The extracted regex pattern
		self.print_with_color("YELLOW","\n\nThe extracted regex pattern is: %s" % regex[0])

		print("\n\nThe provided url example:")
		if len(url_example) > 1:
			for url in url_example:
				self.print_with_color("GREEN", "%s\n" % url)
		else:
			self.print_with_color("GREEN", "%s\n" % url_example[0])

		print("We will try to match against:\n")
		for u in test_urls :
			self.print_with_color("GREEN",ColorsClass.UNDERLINE + "%s " % u )

		successes = 0
		failures  = 0
		# Should match against urls
		for u in test_urls:
			self.print_info("\nMatching for %s ..." % u)
			res = regex[1].match(u)
			if res:
				self.print_success("Match success!: ")
				successes += 1
				print("\n")
			else:
				self.print_failure("Match failed.")
				failures += 1

		self.print_with_bold_color("BLUE", "\n\nTest done with : success : %d  |  failures : %d" % (successes, failures))
