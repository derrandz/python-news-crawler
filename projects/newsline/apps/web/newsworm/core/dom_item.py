from newsline.helpers import helpers

class DomItem:
	"""A doc item is a crawlable item that is identified by a link, a dom path, and a general regex to match all the similar links"""

	def __init__(self, name, url, domselector, nested_items=None):
		self.url = url
		self.name = name
		self.domselector = domselector
		self.nested_items = nested_items
	
	@property
	def url(self):
		return self._url

	@url.setter
	def url(self, url):
		if not url or url is None: raise Exception("url cannot be empty or None")
		if helpers.is_str(url): 
			if not helpers.is_url(url): 
				raise Exception("url should respect the form a url e.g: http://google.com\n\t url: %s"% url)
		if helpers.is_list(url):
			if helpers.is_empty(url):
				raise Exception("url list can not be empty")
			elif not all(helpers.is_str(u) for u in url):
				raise Exception("url is list, expecting all list elements to be str, however an element (or more) is not")
			elif not helpers.is_url(url):
				raise Exception("url list given, however an element does not respect url pattern. e.g: http://google.com\n\t url: %s"% url)

		self._url = url

	@property
	def name(self):
		return self._name
	
	@name.setter
	def name(self, name):
		if not name or name is None: raise Exception("name cannot be empty or None")
		if not helpers.is_str(name): raise Exception("name is expected to be string, %s given" % type(name))
		self._name = name

	@property
	def domselector(self):
		return self._domselector

	@domselector.setter
	def domselector(self, ds):
		if ds is None: raise Exception("domselector cannot be empty or None")
		if helpers.is_list(ds):
			if helpers.is_empty(ds): raise Exception("domselector received an empty list, domselector can not be empty")
			if not all(helpers.is_str(d) for d in ds): raise Exception("domselector received an empty list, but not all elements are strings")
		elif not helpers.is_str(ds): raise Exception("domselector is expected to be a string, %s given"%type(ds))

		if not helpers.is_str(ds) and not helpers.is_list(ds): raise Exception("domselector is expected to be a string or list of strings, %s given"%type(ds))

		self._domselector = ds

	@property
	def nested_items(self):
		return self._nested_items

	@nested_items.setter
	def nested_items(self, ni):
		from newsline.helpers import helpers

		if ni is None: self._nested_items = False
		elif helpers.is_dict(ni):
			try:
				self._nested_items = DomItem(ni['name'], ni['url'], ni['selector'], ni['nested_items']) if 'nested_items' in ni else DomItem(ni['name'], ni['url'], ni['selector'])
			except Exception as e:
				raise Exception("DomItem nested element exception : %s" % str(e))

		elif helpers.is_list(ni):
			if helpers.is_empty(ni):
				raise Exception("nested_items can not be empty")
			elif not all(helpers.is_dict(i) for i in ni):
				raise Exception("nested_items received as list expects all elements to be dict, some aren't")
			try:
				self._nested_items = [DomItem(i['name'], i['url'], i['selector'], i['nested_items']) if 'nested_items' in i else DomItem(i['name'], i['url'], i['selector']) for i in ni]
			except Exception as e:
				raise Exception("DomItem nested element exception : %s" % str(e))

	@property
	def has_nested_items(self):
		return self.nested_items if not self.nested_items else True
	
	@property
	def regexr(self):
		return self._regexr

	@regexr.setter
	def regexr(self, rp):
		self._regexr = rp

	def patternize(self):
		""" This method will extract the regex pattern of the url as to get all similar links."""
		from .regexr import RegexrClass
		self.regexr = RegexrClass(self.url)

		if self.has_nested_items:
			if helpers.is_list(self.nested_items):
				for item in self.nested_items:
					item.patternize()
			else:
				self.nested_items.patternize()

	def getattr_recursive(self, attr, depth=0):
		if not hasattr(self, attr): raise Exception("DomItem object has no attribute %s", str(attr))
		if attr == 'nested_items': raise Exception("nested_items key is not allowed to be fetched recursively")
		if self.has_nested_items:
			if helpers.is_list(self.nested_items):
				return {
					"level_%d"%depth		: getattr(self, attr), 
					"nested_item_%s"%attr   : [ni.getattr_recursive(attr, depth+1) for ni in self.nested_items] 
				}
			else: 
				return {
					"level_%d"%depth		: getattr(self, attr), 
					"nested_item_%s"%attr   : self.nested_items.getattr_recursive(attr, depth+1) 
				}
		else:
			return {"level_%d"%depth: getattr(self, attr)}

	def match(self, url, strength=0):
		if hasattr(self, "_regexr"):
			if strength == 'smart': return self.regexr.smartmatch(url)
			if strength == 0: return True if self.regexr.strongmatch(url) else False
			if strength == 1: return True if self.regexr.shallowmatch(url) else False
			raise Exception("strength attribute expects 0 for strong [default], 1 for shallow, 'smart' for smart, do not specify other than that.")
		return None

	def __repr__(self):
		return "{'name': %s, 'url': %s, 'domselector': %s, 'nested_items': %s}"	% (self.name, self.url, self.domselector, self.nested_items)

	def __str__(self):
		return "{'name': %s, 'url': %s, 'domselector': %s, 'nested_items': %s}"	% (self.name, self.url, self.domselector, self.nested_items)