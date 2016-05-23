from newsline.functionalities.tests.base_simple_test import BaseSimpleTestCase
from newsline.helpers.colors_class import ColorsClass
from newsline.apps.web.newsworm.core.tree import Tree

class TreeTestCase(BaseSimpleTestCase):
	''' A test suit for the Tree class. '''

	def testDepth(self):
		# 0 
		try:
			tree = Tree("Root")
			tree.children = Tree("First Element")
			tree.children[0].children = Tree("Second Element")
		except Exception as e:
			self.print_failure("\t# 0: Test failed with :%s"%str(e))
			self.print_seperator()
		else:
			depth = tree.depth
			if depth == 3:
				self.print_success("# 0 Test passed. Depth of tree is %d"% depth)
				self.print_with_color("DARKCYAN", "%s" % str(tree))
				self.print_seperator()
			else:
				self.print_failure("# 0 Test failed. calculated depth of tree is %d while expecting 3"% depth)
				self.print_with_color("DARKCYAN", "Tree : %s"% str(tree))
				self.print_seperator()

		# 1
		try:
			tree = Tree("Root", children=Tree("First Element", children=Tree("Second Element")))
		except Exception as e:
			self.print_failure("\t# 1: Test failed with :%s"%str(e))
			self.print_seperator()
		else:
			depth = tree.depth
			if depth == 3:
				self.print_success("# 1 Test passed. Depth of tree is %d"% depth)
				self.print_with_color("DARKCYAN", "%s" % str(tree))
				self.print_seperator()
			else:
				self.print_failure("# 1Test failed. calculated depth of tree is %d while expecting 3"% depth)
				self.print_with_color("DARKCYAN", "%s" % str(tree))
				self.print_seperator()

		# 2
		try:
			tree = Tree("Root", children=[
				Tree("Branch1 El1"),
				Tree("Branch1 El2", children=[
					Tree("Branch2 El1"),
					Tree("Branch2 El2"),
					Tree("Branch2 El3", children=[
						Tree("Branch3 El1"),
						Tree("Branch3 El2"),
						Tree("Branch3 El3", children=Tree("Branch4 El1")),
					]),
				])
			])
		except Exception as e:
			self.print_failure("\t# 3: Test failed with :%s"%str(e))
			self.print_seperator()
		else:
			depth = tree.depth
			if depth == 5:
				self.print_success("# 3 Test passed. Depth of tree is %d"% depth)
				self.print_with_color("DARKCYAN", "%s" % str(tree))
				self.print_seperator()
			else:
				self.print_failure("# 3: Test failed. calculated depth of tree is %d while expecting 5"% depth)
				self.print_with_color("DARKCYAN", "%s" % str(tree))
				self.print_seperator()

	def setUpTest(self):
		# 0
		self.print_info("The following test should fail. | Supplying None as for data as an argument")
		try:
			Tree(None)
		except Exception as e:
			self.print_failure("\t# 0: Test failed with :%s"%str(e))
			self.print_seperator()
			raised = True
		else:
			self.print_success("\t# 0: Test passed.")
			self.print_seperator()

		# 1
		self.print_info("The following test should fail. | supplying empty strings for data and level as arguments")
		try:
			Tree("", "")
		except Exception as e:
			self.print_failure("\t# 1: Test failed with :%s"%str(e))
			self.print_seperator()
			raised = True
		else:
			self.print_success("\t# 1: Test passed.")
			self.print_seperator()

		# 2
		self.print_info("The following test should pass. | Supplying proper <str> data and level <int>")
		try:
			tree = Tree("TreeElement", 1)
		except Exception as e:
			self.print_failure("\t# 2: Test failed with :%s"%str(e))
			self.print_seperator()
		else:
			self.print_success("\t# 2: Test passed.")
			self.print_seperator()

		# 3
		self.print_info("The following test should fail | Adding a list of children in which an element is not tree <int>")
		try:
			tree = Tree("ROOT")
			tree.children = [Tree("First Child"), Tree("Second Child"), 1]
		except Exception as e:
			self.print_failure("\t# 3: Test failed with :%s"%str(e))
			self.print_seperator()
		else:
			self.print_success("\t# 3: Test passed.")
			self.print_seperator()

		# 4
		self.print_info("The following test should pass and print correct depths | supplying list of children with an element having nested node")
		try:
			tree = Tree("ROOT")
			tree.children = [Tree("First Child"), Tree("Second Child", children=[Tree("Second Element's nested node")])]
		except Exception as e:
			self.print_failure("\t# 4: Test failed with :%s"%str(e))
			self.print_seperator()
		else:
			self.print_success("\t# 4: Test passed.")
			self.print_success("\n\n %s" % str(tree))
			self.print_seperator()

	def printtreeTest(self):
		# 4
		self.print_info("The following test should pass and print correct depths | supplying list of children with an element having nested node")
		try:
			tree = Tree("ROOT")
			tree.children = [Tree("First Child"), Tree("Second Child", children=[Tree("Second Element's nested node")])]
		except Exception as e:
			self.print_failure("\t# 4: Test failed with :%s"%str(e))
			self.print_seperator()
		else:
			self.print_success("\t# 4: Test passed.")
			self.print_success("\n\n %s" % tree.printtree())
			self.print_seperator()

	def testDivergence(self):
		try:
			tree = Tree("Root", children=[
					Tree("FirstNode"),
					Tree("SecondNode"),
					Tree("ThirdNode", children=[
						Tree("_FirstNode")
					])
				])

		except Exception as e:
			self.print_failure("\t#Instantiatino failed with :%s"%str(e))
			self.print_seperator()
			raised = True
		else:
			self.print_success("\tInstantiation passed.")

			def _dumfn(thisTree):
				print("Tree with %s and %s." % (thisTree.level, thisTree.data))

			tree.diverge(_dumfn)
