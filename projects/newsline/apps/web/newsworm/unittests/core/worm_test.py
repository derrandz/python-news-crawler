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
	def save_crawl_results(self, name, results):
		from newsline.helpers import helpers
		helpers.write_json(name, results)

	def read_from_training_data(self):
		from newsline.helpers import helpers
		from django.conf import settings
		return helpers.parse_json_file(settings.NEWSLINE_DIR +"/apps/web/newsworm/unittests/core/_files/_input/training_set.json")

	def wormTestValidate(self):
		class WormTestClass(Worm):
			def __init__(self, rooturl=None, domitems=None):
				self.regexr = RegexrClass()
				self.rooturl = rooturl
				self.temp = self.validate(domitems)
		

		# 0
		raised = False
		try:
			self.print_info("# 0: The following test should fail.")
			from copy import deepcopy
			worm = WormTestClass("http://www.goud.ma/", 1)
		except Exception as e:
			raised = True
			self.print_failure("# 0: Test failed with :%s"%str(e))

		if not raised:
			self.print_success("# 0: Test passed")


		# 1
		raised = False
		self.print_seperator()
		try:
			self.print_info("# 1: The following test should fail.")
			from copy import deepcopy
			worm = WormTestClass("http://www.goud.ma/", [1, {}])
		except Exception as e:
			raised = True
			self.print_failure("# 1: Test failed with :%s"%str(e))

		if not raised:
			self.print_success("# 1: Test passed")

		# 2
		raised = False
		self.print_seperator()
		try:
			self.print_info("# 2: The following test should pass.")
			from copy import deepcopy
			worm = WormTestClass("http://www.goud.ma/", [{}, {}])
		except Exception as e:
			raised = True
			self.print_failure("# 2: Test failed with :%s"%str(e))

		if not raised:
			self.print_success("# 3: Test passed")


	def wormTestNormalize(self):

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

	def wormTestDecode(self):

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

	def wormTestClean(self):

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

	def wormTestNormalizationPhase(self):

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