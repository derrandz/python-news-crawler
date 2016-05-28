from django.test import SimpleTestCase
from newsline.functionalities.tests.base_simple_test import BaseSimpleTestCase

from . import helpers

class HelpersTestCase(BaseSimpleTestCase):

	def mapDictionarySingleKeyTestCase(self):
		mydict = {
			"a": 1,
			"b": 'b',
			"dictkey": {
				"a": 1,
				"b": 'b',
				"b_dictkey":{
					"a": 1,
					"b": 'b'
				}
			}
		}

		def addone(a):
			return a + 1

		mydict = helpers.map_dictionary(addone, mydict, "a")

		self.print_with_color("DARKCYAN", "\n[PreMap]: dictionary\n\t%s" % mydict)
		self.print_with_color("DARKCYAN", "\n[PostMap]: Dictionary\n\t%s" % mydict)

	def mapDictionaryListKeyTestCase(self):
		mydict = {
			"a": 1,
			"b": 1,
			"c": 1,
			"d": 'd',
			"dictkey": {
				"a": 1,
				"b": 1,
				"c": 1,
				"d": 'd',
				"b_dictkey":{
					"a": 1,
					"b": 1,
					"c": 1,
					"d": 'd'
				}
			}
		}

		def addone(a):
			return a + 1

		mydict = helpers.map_dictionary(addone, mydict, ["a", "b", "c"])

		self.print_with_color("DARKCYAN", "\n[PreMap]: dictionary\n\t%s" % mydict)
		self.print_with_color("DARKCYAN", "\n[PostMap]: Dictionary\n\t%s" % mydict)

	def mapDictionaryNestedListTestCase(self):
		mydict = {
			"a": 1,
			"b": 10,
			"nested_list": [
				{"a": 1, "c": 20},
				{"c": 12, "d": 25}
			]
		}

		def addone(a):
			return a + 1

		self.print_with_color("DARKCYAN", "\n[PreMap]: dictionary\n\t%s" % mydict)
		
		mydict = helpers.map_dictionary(addone, mydict, ["c", "d"])
		self.print_with_color("DARKCYAN", "\n[PostMap]: Dictionary\n\t%s" % mydict)

	def isUrlTest(self):
		urls = ["/url", "http://www.url.com", "www.url.com", "#"]

		for u in urls:
			if helpers.is_url(u): self.print_success("Matched %s" % u)
			else : self.print_failure("Did not match %s" % u)

