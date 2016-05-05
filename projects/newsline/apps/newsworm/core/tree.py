
class Tree:

	"""Generic tree node."""

	def __init__(self, depth=0, content=None, children=None):
		self.depth = depth

		# This piece of code can be written in a more optimized way you could say.
		# I agree, but I am interested in the print.
		if content is not None:
			self.content = content
		else:
			print('The node expect a string content, None given.')
			assert False
			 
		if children is not None:
			for child in children:
				self.add_child(child)

	def __repr__(self):
		return 'The depth of this node is : %d ' % self.depth

	def add_child(self, node):
		assert isinstance(node, Tree)
		self.children.append(node)