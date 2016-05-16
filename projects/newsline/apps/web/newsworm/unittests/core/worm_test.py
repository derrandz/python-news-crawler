import re

from htmldom import htmldom
from newsline.apps.web.newsworm.core.worm import Worm
from django.test import SimpleTestCase
from newsline.helpers.colors_class import ColorsClass
from newsline.functionalities.tests.base_simple_test import BaseSimpleTestCase
from newsline.apps.web.newsworm.core.regexr import RegexrClass

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
		return helpers.parse_json_file("./newsline/apps/web/newsworm/unittests/core/_files/_input/training_set.json")

	def test_crawl(self, index):
		_data = self.read_from_training_data()
		if index in _data:
			_data = _data[index]
		else:
			raise ValueError("Training data dictionary does not contain key: %s" % index)

		worm = Worm(_data["root_url"], _data)
		_crawl_results = worm.launch()

		if __name__ == "__main__" :
			try:
				_crawl_results = worm.launch()
			except:
				worm.logger.close_logging_session()
		else:
			_crawl_results = worm.launch()

		self.print_results(_crawl_results, worm.is_category_multipage())
		self.save_crawl_results("./newsline/apps/web/newsworm/unittests/core/_files/_output/%s_crawl_results.json" % index, _crawl_results)

	def test_save(self):
		from newsline.helpers import helpers
		# helpers.prettify_json_file("./newsline/apps/newsworm/unittests/core/_files/_input/training_set.json")

	def test_website(self):
		self.test_crawl("horiapress") # open ./_files/input/training_data.json for precise info