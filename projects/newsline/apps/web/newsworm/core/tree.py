from newsline.helpers import helpers

class Tree:
	"""Generic tree node."""

	def __init__(self, data="", level=0, children=None):
		self.data = data
		self.level = level
		self.children = children

	@property
	def data(self):
		return self._data

	@data.setter
	def data(self, dt):
		if dt is None: raise Exception("Data can not be none")
		self._data = dt

	@property
	def level(self):
		return self._level

	@level.setter
	def level(self, l):
		if l is None: raise Exception("Level can not be None")
		if not isinstance(l, int): raise Exception("Level is expected to be a digit, %s given" % type(l))
		self._level = l
	
	def update_level(self, l):
		self.level = l
		if self.children:
			if helpers.is_list(self.children):
				for child in self.children:
					child.update_level(l+1)
			elif isinstance(self.children, Tree):
				self.children.update_level(l+1)

	@property
	def children(self):
		return self._children

	@children.setter
	def children(self, xchildren):
		if xchildren is None or xchildren == []:
			self._children = []
			return None
		else:
			if not hasattr(self, '_children'): self._children = []
			self._add(xchildren)

	def _add(self, xchildren):
		def _update_level(obj, l):
			obj.update_level(l)
			return obj

		if not helpers.is_list(xchildren):
			if not isinstance(xchildren, Tree): 
				raise Exception("Children are expected to be of type Tree, %s given"% type(xchildren))
			else:
				self._children.append(_update_level(xchildren, self.level + 1))
		else:
			if not all(isinstance(c, Tree) for c in xchildren): 
				raise Exception("Children list is expected to have all elements of type Tree, some aren't")
			else:
				self._children.extend([_update_level(child, self.level + 1) for child in xchildren])
		
	@property
	def depth(self):
		return self._calculatedepth()

	def _calculatedepth(self):
		if self.children:
			level = self.level # just for initialization purposes
			for child in self.children:
				level = child.depth if child.depth > level else level
			return level if self.level > 0 else level + 1
		else:
			return self.level	
	
	def __repr__(self):
		return 'Tree element with data: %s and level: %s ' % (self.data, self.level)

	def __str__(self):
		treebuffer = "\n%s{data: %s, level: %d" % (helpers.indent(self.level+1), self.data, self.level)

		if not self.children: treebuffer += "},\n" if self.level else "}\n"
		else:
			for child in self.children:
				treebuffer += str(child)

		return treebuffer if self.level else treebuffer + "\n\t}\n"