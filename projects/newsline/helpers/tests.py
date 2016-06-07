from django.test import SimpleTestCase
from newsline.functionalities.tests.base_simple_test import BaseSimpleTestCase

from . import helpers

class HelpersTestCase(BaseSimpleTestCase):

	def testMapDictionarySingleKey(self):
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


		self.print_with_color("DARKCYAN", "\n[PreMap]: dictionary\n\t%s" % mydict)
		mydict = helpers.map_dictionary(addone, mydict, "a")
		self.print_with_color("DARKCYAN", "\n[PostMap]: Dictionary\n\t%s" % mydict)

	def testMapDictionaryNoKey(self):
		mydict = {
			"a": 1,
			"b": 2,
			"dictkey": {
				"a": 1,
				"b": 2,
				"b_dictkey":{
					"a": 1,
					"b": 2
				}
			}
		}

		def addone(a):
			return a + 1


		self.print_with_color("DARKCYAN", "\n[PreMap]: dictionary\n\t%s" % mydict)
		mydict = helpers.map_dictionary(addone, mydict)
		self.print_with_color("DARKCYAN", "\n[PostMap]: Dictionary\n\t%s" % mydict)

	def testMapDictionaryListKey(self):
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

	def testMapDictionaryNestedList(self):
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

	def testWalkDict1(self):
		mydict = {
			"First":{
				"first a": "a",
				"first b": "b",
				"first c": "c"
			},

			"Second":{
				"second a" : "a",
				"second b" : "b",
				"second c" : "c"
			},

			"Third":{
				"third a" : "a",
				"third b" : "b",
				"third c" : "c"
			},

			"Forth":{
				"forth a" : "a",
				"forth b" : "b",
				"forth c" : "c"
			}

		}

		def testfn(dictel):
			print(dictel)
			self.print_seperator()
		
		mydict = helpers.walk_dictionary(mydict, testfn)

	def testWalkDict2(self):
		mydict = {
			"First":{
				"first a": "a",
				"first b": "b",
				"type": "type1",
				"nested_el": {
					"type": "type2"
				}
			},

			"Second":{
				"second a" : "a",
				"second b" : "b",
				"type": "type3"
			},

			"Third":{
				"third a" : "a",
				"third b" : "b",
				"type" : "type4",
				"nested_el": {
					"type" : "type6",
					"nested_el": {
						"type" : "type5"
					}
				}
			},

			"Forth":{
				"forth a" : "a",
				"forth b" : "b",
				"type" : "type7"
			}

		}

		def getKeyVal(dictel):
			if 'type' in dictel:
				print("Found %s : %s" % ('type', dictel['type']))
		
		mydict = helpers.walk_dictionary(mydict, getKeyVal)

	def testIsUrl(self):
		urls = ["/url", "http://www.url.com", "www.url.com", "#"]

		for u in urls:
			if helpers.is_url(u): self.print_success("Matched %s" % u)
			else : self.print_failure("Did not match %s" % u)

	def testWriteJson(self):
		dictionary = {
			"1": "one",
			"2": "two",
			"3": "three"
		}

		from django.conf import settings
		helpers.write_json(settings.NEWSLINE_DIR + "/helpers/test_writejson.json", dictionary)

	def testParseJsonFile(self):
		from django.conf import settings
		jsonfile = helpers.parse_json_file(settings.NEWSLINE_DIR + "/helpers/parsejsontestfile.json")

		print("%s" % jsonfile)