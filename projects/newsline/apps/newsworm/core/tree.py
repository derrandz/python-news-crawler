
class Tree:

	"""Generic tree node."""

	def __init__(self, depth=0, content=None, children=None, is_root=False, tree_depth_size=None):
		self.depth = depth
		self.is_root = is_root

		if self.is_root:
			assert( tree_depth_size is not None)
			self.tree_depth_size = tree_depth_size

		# This piece of code can be written in a more optimized way you could say.
		# I agree, but I am interested in the print.
		if content is not None:
			self.content = content
		else:
			print('The node expect a string content, None given.')
			assert False

		self.children = [] 
		if children is not None:
			for child in children:
				self.add_child(child)

	def __repr__(self):
		return 'The depth of this node is : %d ' % self.depth

	def increment_size(self):
		assert self.is_root
		self.tree_depth_size += 1
		return self.tree_depth_size

	def add_child(self, node):
		assert isinstance(node, Tree)
		self.children.append(node)