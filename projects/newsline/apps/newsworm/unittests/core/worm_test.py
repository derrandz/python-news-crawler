import re

from htmldom import htmldom
from newsline.apps.newsworm.core.worm import Worm
from django.test import SimpleTestCase
from newsline.apps.newsworm.unittests.colors_class import ColorsClass
from newsline.apps.newsworm.unittests.base_simple_test import BaseSimpleTestCase
from newsline.apps.newsworm.core.regexr import RegexrClass

class WormTestCase(BaseSimpleTestCase):
	'''
	A test suit for the worm class.
	
	Not the best tests in the world, codewise, but they test wsup.
	'''

	def save_crawl_results(self, name, results):
		from newsline.apps.newsworm.core import helpers
		helpers.write_json(name, results)

	def read_from_training_data(self):
		from newsline.apps.newsworm.core import helpers
		return helpers.parse_json_file("./newsline/apps/newsworm/unittests/core/_files/_input/training_set.json")

	def test_crawl(self, index):
		_data = self.read_from_training_data()
		if index in _data:
			_data = _data[index]
		else:
			raise ValueError("Training data dictionary does not contain key: %s" % index)

		worm = Worm(_data["root_url"], _data)
		_crawl_results = worm.launch()
		self.save_crawl_results("./_files/_output/%s_crawl_results" % index, _crawl_results)

	def test_save(self):
		from newsline.apps.newsworm.core import helpers
		helpers.prettify_json_file("./newsline/apps/newsworm/unittests/core/_files/_input/training_set.json")

	def test_website(self):
		self.test_crawl("hespress") # open ./_files/input/training_data.json for precise info