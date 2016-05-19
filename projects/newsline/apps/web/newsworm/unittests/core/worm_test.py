from htmldom import htmldom
from django.test import SimpleTestCase
from newsline.apps.web.newsworm.core.worm import Worm
from newsline.helpers.colors_class import ColorsClass
from newsline.functionalities.tests.base_simple_test import BaseSimpleTestCase
from newsline.apps.web.newsworm.core.regexr import RegexrClass

import re

class WormTestCase(BaseSimpleTestCase):
	'''
	A test suit for the worm class.
	
	Not the best tests in the world, codewise, but they test wsup.
	'''
	def print_results(self, results, multipage=False):
		self.print_with_color("CYAN", "---------------------- Results ----------------------")
		self.print_with_color("CYAN", "- Category Regex ----------------------:\n\t%s"%results["category_regex_pattern"])
		self.print_with_color("CYAN", "- Article Regex ----------------------:\n\t%s"%results["article_regex_pattern"])
		self.print_with_color("CYAN", "- NextPage Regex ----------------------:\n\t%s"%results["nextpage_regex_pattern"])
		if multipage:
			for ckey, category in results["results"].items():
				self.print_with_color("CYAN", "\nCategory: %s" % ckey)
				for pkey, page in category.items():
					self.print_with_color("YELLOW", "\n\tPage: %s" % pkey)
					for article in page:
						self.print_with_color("GREEN", "\n\t\tArticle: %s" % article)
		else:
			for ckey, category in results["results"].items():
				self.print_with_color("CYAN", "\nCategory: %s" % ckey)
				for article in category:
					self.print_with_color("GREEN", "\n\tArticle: %s" % article)


	def save_crawl_results(self, name, results):
		from newsline.helpers import helpers
		helpers.write_json(name, results)

	def read_from_training_data(self):
		from newsline.helpers import helpers
		from django.conf import settings
		return helpers.parse_json_file(settings.NEWSLINE_DIR +"/apps/web/newsworm/unittests/core/_files/_input/training_set.json")

	def test_crawl(self, index):
		_data = self.read_from_training_data()
		if index in _data:
			_data = _data[index] # Fetches the dictionary at the specified index
		else:
			raise ValueError("Training data dictionary does not contain key: %s" % index)

		worm = Worm(_data["root_url"], _data)
		_crawl_results = worm.launch()

		if _crawl_results["status"]:
			self.print_success("Crawled %s with success."% _data["root_url"])
		else:
			self.print_failure("Failed to crawl %s."% _data["root_url"])

		self.print_results(_crawl_results, worm.is_category_multipage())

		from django.conf import settings
		self.save_crawl_results(settings.NEWSLINE_DIR + "/apps/web/newsworm/unittests/core/_files/_output/%s_crawl_results.json" % index, _crawl_results)

	def test_save(self):
		from newsline.helpers import helpers
		helpers.prettify_json_file(settings.NEWSLINE_DIR + "/newsline/apps/newsworm/unittests/core/_files/_input/training_set.json")

	def test_website(self):
		self.test_crawl("hespress") # open ./_files/input/training_data.json for precise info

	def test_addrooturl(self):
		rooturl ="http://www.root.com/"
		worm = Worm(rooturl, None, ignore_validation=True, nocrawl=True)
		examples = ["/cat1/cat2", "cat2/cat3", "//cat23/cat22//"]
		expected = ["/cat1/cat2", "/cat2/cat3", "/cat23/cat22"]

		l = list(map(worm.add_rooturl, examples))
		for i, el in enumerate(l):
			self.print_with_color("BOLD", "Arg Supplied: %s, Result: %s, Expected: %s"% (examples[i], el, rooturl.strip("/")+expected[i]))

	def wormTestN(self):
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
		worm = Worm("http://www.goud.ma/", deepcopy(domitems))
		self.print_with_color("DARKCYAN", "\n[PreNormaliziation]: %s"% domitems)
		self.print_with_color("DARKCYAN", "\n[PostNormalization]: %s"% worm.temp)