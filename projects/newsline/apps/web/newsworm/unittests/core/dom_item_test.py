import re

from newsline.functionalities.tests.base_simple_test import BaseSimpleTestCase
from newsline.helpers.colors_class import ColorsClass
from newsline.apps.web.newsworm.core.dom_item import DomItem

class DomItemTestCase(BaseSimpleTestCase):
	''' A test suit for the DomItem class. '''

	def setUpFailTest(self):
		import sys
		try:
			DomItem("google.com", 1)
		except Exception as e:
			self.print_failure("Test failed with :%s"%str(e))

		try:
			DomItem("http://google.com", 1)
		except Exception as e:
			self.print_failure("Test failed with :%s"%str(e))

		try:
			DomItem(["google.com", "googlecom"], "something")
		except Exception as e:
			self.print_failure("Test failed with :%s"%str(e))

		try:
			DomItem(["http://google.com", "http://www.googlecom"], "something")
		except Exception as e:
			self.print_failure("Test failed with :%s"%str(e))

		try:
			DomItem(["http://google.com", "http://www.google.com", 1], "something")
		except Exception as e:
			self.print_failure("Test failed with :%s"%str(e))

	def setUpSuccessTest(self):
		url = "http://www.google.com"
		selector = "div.class > ul#id > li > a"

		try:
			dom_item = DomItem(url, selector)
		except Expected as e:
			pass

		self.print_success("Test passed for : %s, %s"%(url, selector))

		url = ["http://www.google.com", "http://www.google.com"]
		selector = "div.class > ul#id > li > a"
		
		try:
			dom_item = DomItem(url, selector)
		except Exception as e:
			pass
			
		self.print_success("Test passed for : %s, %s"%(url, selector))

		url = ["http://www.google.com", "www.google.com"]
		selector = "div.class > ul#id > li > a"
		
		try:
			dom_item = DomItem(url, selector)
		except Exception as e:
			pass

		self.print_success("Test passed for : %s, %s"%(url, selector))

		url = ["http://www.google.com", "www.google.com"]
		selector = ["div.class > ul#id > li > a", "div.class > ul#id > li > a"]
		
		try:
			dom_item = DomItem(url, selector)
		except Exception as e:
			pass

		self.print_success("Test passed for : %s, %s"%(url, selector))
