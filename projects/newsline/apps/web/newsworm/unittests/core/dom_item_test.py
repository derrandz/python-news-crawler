import re

from newsline.functionalities.tests.base_simple_test import BaseSimpleTestCase
from newsline.helpers.colors_class import ColorsClass
from newsline.apps.web.newsworm.core.dom_item import DomItem

class DomItemTestCase(BaseSimpleTestCase):
	''' A test suit for the DomItem class. '''
	
	def setUpFailTest(self):
		# 0
		try:
			DomItem("", "google.com", 1)
		except Exception as e:
			self.print_failure("# 0: Test failed with :%s"%str(e))
			self.print_seperator()
		else:
			self.print_success("# 0: Test passed.")
			self.print_seperator()

		# 1
		try:
			DomItem("clickablebutton", "google.com", 1)
		except Exception as e:
			self.print_failure("# 1: Test failed with :%s"%str(e))
			self.print_seperator()
		else:
			self.print_success("# 1: Test passed.")
			self.print_seperator()

		# 2
		try:
			DomItem("clickablebutton", "http://google.com", 1)
		except Exception as e:
			self.print_failure("# 2: Test failed with :%s"%str(e))
			self.print_seperator()
		else:
			self.print_success("# 2: Test passed.")
			self.print_seperator()

		# 3
		try:
			DomItem("clickablebutton", ["google.com", "googlecom"], "something")
		except Exception as e:
			self.print_failure("# 3: Test failed with :%s"%str(e))
			self.print_seperator()
		else:
			self.print_success("# 3: Test passed.")
			self.print_seperator()

		# 4
		try:
			DomItem("clickablebutton", ["http://google.com", "http://www.googlecom"], "something")
		except Exception as e:
			self.print_failure("# 4: Test failed with :%s"%str(e))
			self.print_seperator()
		else:
			self.print_success("# 4: Test passed.")
			self.print_seperator()

		# 5
		try:
			DomItem("clickablebutton", ["http://google.com", "http://www.google.com", 1], "something")
		except Exception as e:
			self.print_failure("# 5: Test failed with :%s"%str(e))
			self.print_seperator()
		else:
			self.print_success("# 5: Test passed.")
			self.print_seperator()

		# 6
		try:
			DomItem("clickablebutton", "http://google.com","div.class > a", {"url": 'http://google.com', "selector":'div.class', 'nested_items': []})
		except Exception as e:
			self.print_failure("# 6: Test failed with :%s"%str(e))
			self.print_seperator()
		else:
			self.print_success("# 6: Test passed.")
			self.print_seperator()

	def setUpSuccessTest(self):
		name = "an item's name"
		url = "http://www.google.com"
		selector = "div.class > ul#id > li > a"

		# 1
		try:
			dom_item = DomItem(name, url, selector)
		except Exception as e:
			self.print_failure("# 1: Test failed with :%s"%str(e))
			self.print_seperator()
		else:
			self.print_success("Test passed for : %s, %s, %s"%(name, url, selector))
			self.print_seperator()

		# 2
		url = ["http://www.google.com", "http://www.google.com"]
		selector = "div.class > ul#id > li > a"
		try:
			dom_item = DomItem(name, url, selector)
		except Exception as e:
			self.print_failure("# 2: Test failed with :%s"%str(e))
			self.print_seperator()
		else:
			self.print_success("# 2: Test passed for : %s, %s, %s"%(name, url, selector))
			self.print_seperator()

		# 3
		url = ["http://www.google.com", "www.google.com"]
		selector = "div.class > ul#id > li > a"
		try:
			dom_item = DomItem(name, url, selector)
		except Exception as e:
			self.print_failure("# 3: Test failed with :%s"%str(e))
			self.print_seperator()
		else:
			self.print_success("# 3: Test passed for : %s, %s, %s"%(name, url, selector))
			self.print_seperator()
		# 4
		url = ["http://www.google.com", "www.google.com"]
		selector = ["div.class > ul#id > li > a", "div.class > ul#id > li > a"]
		
		try:
			dom_item = DomItem(name, url, selector)
		except Exception as e:
			self.print_failure("# 4: Test failed with :%s"%str(e))
			self.print_seperator()
		else:
			self.print_success("# 4: Test passed for : %s, %s, %s"%(name, url, selector))
			self.print_seperator()

		# 5
		url = ["http://www.google.com", "www.google.com"]
		selector = ["div.class > ul#id > li > a", "div.class > ul#id > li > a"]
		nested_items = {"name": 'nesteditem',"url":'www.google.com', "selector":'div.class > li > a'}
		try:
			dom_item = DomItem("myname", url, selector, nested_items)
		except Exception as e:
			self.print_failure("# 5: Test failed with :%s"%str(e))
			self.print_seperator()
		else:
			self.print_success("# 5: Test passed for : %s, %s, %s, %s"%(name, url, selector, nested_items))
			self.print_seperator()

		# 6
		url = ["http://www.google.com", "www.google.com"]
		selector = ["div.class > ul#id > li > a", "div.class > ul#id > li > a"]
		nested_items = [
			{"name": 'nesteditem', "url":'www.google.com', "selector":'div.class > li > a'},
			{"name": 'nesteditem', "url":'/sub/url1', "selector":'div.class > li > a'},
			{"name": 'nesteditem', "url":'/sub/url2', "selector":'div.class > li > a'},
			{
				"name": 'nesteditem',
				"url":'/sub/url3', 
				"selector":'div.class > li > a', 
				"nested_items": {"name": 'nesteditem', "url":'/page1', "selector":'div.class > li > a'}
			}
		]
		try:
			dom_item = DomItem(name, url, selector, nested_items)
		except Exception as e:
			self.print_failure("# 6: Test failed with :%s"%str(e))
			self.print_seperator()
		else:
			self.print_success("# 6: Test passed for : %s, %s, %s, %s"%(name, url, selector, nested_items))
			self.print_seperator()

		# 7
		url = ["http://www.google.com", "www.google.com"]
		selector = ["div.class > ul#id > li > a", "div.class > ul#id > li > a"]
		nested_items = [
			{
				"name": 'nesteditem', 
				"url":'/sub/url3', 
				"selector":'div.class > li > a', 
				"nested_items": [
					{"name": 'nesteditem', "url":'/page1', "selector":'div.class > li > a'},
					{"name": 'nesteditem', "url":'/page2', "selector":'div.class > li > a'},
					{"name": 'nesteditem', "url":'/page3', "selector":'div.class > li > a'},
					{
						"name": 'nesteditem', 
						"url":'/page4', 
						"selector":'div.class > li > a',
						"nested_items":[
							{"name": 'nesteditem', "url":'/page4/page1', "selector":'div.class > li > a'},
							{"name": 'nesteditem', "url":'/page4/page2', "selector":'div.class > li > a'},
							{"name": 'nesteditem', "url":'/page4/page3', "selector":'div.class > li > a'}
						]
					},
				]
			}
		]

		try:
			dom_item = DomItem(name, url, selector, nested_items)
		except Exception as e:
			self.print_failure("# 7: Test failed with :%s"%str(e))
			self.print_seperator()
		else:
			self.print_success("# 7: Test passed for : %s, %s, %s, %s"%(name, url, selector, nested_items))
			self.print_seperator()

	def testCasePatternize(self):
		try:
			domitem = DomItem('category_item', '/category/politics', 'nav > ul > li > a')
			domitem.patternize()
		except Exception as e:
			self.print_failure("Test failed with :%s"%str(e))
			self.print_seperator()
			raise e
		else:
			self.print_success("Test passed for : %s, %s, %s, %s"%(domitem.name, domitem.url, domitem.domselector, domitem.regexr.pattern))
			self.print_seperator()


	def realCaseTest(self):
		raised = False
		domitem = None
		try:
			domitem = DomItem('category_item', '/category/politics', 'nav > ul > li > a', {
					"name": 'pagination',
					"url": '/category/politics/page1',
					"selector": 'div.pagination > ul > li > a',
					"nested_items": {
						"name": 'articles',
						"url": '/article/123123.html',
						"selector": 'h2 > a'
					}
				})
		except Exception as e:
			self.print_failure("Test failed with :%s"%str(e))
			self.print_seperator()
			return

		self.print_success("Dom Item instantiation successful")
		
		self.print_with_color("DARKCYAN","DomItem name: %s"% domitem.name)
		self.print_with_color("DARKCYAN","DomItem url: %s"% domitem.url)
		self.print_with_color("DARKCYAN","DomItem selector: %s"% domitem.domselector)
		self.print_with_color("DARKCYAN","DomItem has_nested_items: %s"% domitem.has_nested_items)

		if domitem.has_nested_items:
			self.print_success("\tDom Item has nested items")
			from newsline.helpers import helpers
			if helpers.is_list(domitem.nested_items):
				self.print_with_color("DARKCYAN","\tNested DomItems are many")
			else:
				nitem = domitem.nested_items
				self.print_with_color("DARKCYAN","\tNested DomItem name: %s"% nitem.name)
				self.print_with_color("DARKCYAN","\tNested DomItem url: %s"% nitem.url)
				self.print_with_color("DARKCYAN","\tNested DomItem selector: %s"% nitem.domselector)
				self.print_with_color("DARKCYAN","\tNested DomItem has_nested_items: %s"% nitem.has_nested_items)

				if nitem.has_nested_items:
					self.print_success("\t\tNested Dom Item has nested items")
					from newsline.helpers import helpers
					if helpers.is_dict(nitem.nested_items):
						self.print_with_color("DARKCYAN","\tNested DomItems nested items are many")
					else:
						nnitem = nitem.nested_items
						self.print_with_color("DARKCYAN","\t\tNested DomItem name: %s"% nnitem.name)
						self.print_with_color("DARKCYAN","\t\tNested DomItem url: %s"% nnitem.url)
						self.print_with_color("DARKCYAN","\t\tNested DomItem selector: %s"% nnitem.domselector)
						self.print_with_color("DARKCYAN","\t\tNested DomItem has_nested_items: %s"% nnitem.has_nested_items)

				self.print_success("Test passed successfully")
				self.print_seperator()

	def domItemPatternizeAndMatch(self):
		def _match(matcheables, _type):
			for url in matcheables:
				status = domitem.match(url, _type)
				if status is not None:
					if isinstance(_type, str):
						if status == 0:
							self.print_success("%s Matches!" % url)
						elif status == 1:
							self.print_with_color("DARKCYAN", "%s Matches, but only shallow!" % url)
						else:
							self.print_failure("%s Does not match!" % url)
					else:
						if status:
							self.print_success("%s Matches!" % url)
						else:
							self.print_failure("%s Does not match!" % url)
		try:
			domitem = DomItem('category_item', '/category/politics', 'nav > ul > li > a')
		except Exception as e:
			self.print_failure("Test failed @instantiation with :%s"%str(e))
			self.print_seperator()
		else:
			try:
				domitem.patternize()
			except Exception as e:
				self.print_failure("Test failed @patternize with :%s"%str(e))
				self.print_seperator()
			else:
				self.print_success("patternize succeeded.")
				self.print_success("\nResult:\n\t%s" % domitem.regexr.pattern)
				matcheables = ["/category/news", "/category/something", "/category/accidents", "www.google.com", "/winlottery/subscribe/now"]
				self.print_seperator()
				self.print_info("Smart maching")
				_match(matcheables, 'smart')

				self.print_seperator()
				self.print_info("Strong matching")
				_match(matcheables, 0)

	def domItemPatternizeRecursiveTestCase(self):
		try:
			domitem = DomItem('category_item', '/category/politics', 'nav > ul > li > a', {
					"name": 'pagination',
					"url": '/category/politics/page1',
					"selector": 'div.pagination > ul > li > a',
					"nested_items": {
						"name": 'articles',
						"url": '/article/123123.html',
						"selector": 'h2 > a',
						"nested_items":[
							{"name": 'nesteditem1', "url": '/nesteditem/count1', "selector": 'span > p'},
							{"name": 'nesteditem2', "url": '/nesteditem/count2', "selector": 'span > p'},
							{"name": 'nesteditem3', "url": '/nesteditem/count3', "selector": 'span > p'}
						]
					}
				})
		except Exception as e:
			self.print_failure("Test failed @instantiation with :%s"%str(e))
			self.print_seperator()
		else:
			try:
				domitem.patternize()
			except Exception as e:
				raised = True
				self.print_failure("Test failed @patternize with :%s"%str(e))
				self.print_seperator()

				self.print_success("patternize succeeded.")
				self.print_success("\nResult:\n\t%s" % domitem.getattr_recursive("regexr"))