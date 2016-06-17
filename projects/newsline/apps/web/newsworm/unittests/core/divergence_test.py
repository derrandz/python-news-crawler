from newsline.functionalities.tests.base_simple_test import BaseSimpleTestCase
from newsline.helpers.colors_class import ColorsClass
from newsline.apps.web.newsworm.core.tree import Tree

import newsline.apps.web.newsworm.core.divergence as divergence

class DivergenceTestCase(BaseSimpleTestCase):
	''' A test suit for divergence decorators. '''

	def testClass(self):
		@divergence.divergent("children")
		class TestClass(Tree):
			pass


		try:
			divergentObj = TestClass("Root", children=[
				TestClass("ChildNode1"), 
				TestClass("ChildNode1_2"), 
				TestClass("ChildNode1_3", children=TestClass("ChildNode2_2")) 
			])

			divergentObj.diverge(print)
		except Exception as e:
			self.print_exception(e)
			raise e
		else:
			self.print_success("Test passed")