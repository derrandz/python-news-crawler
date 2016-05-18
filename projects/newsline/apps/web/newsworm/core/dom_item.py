
class DomItem:
	"""A doc item is a crawlable item that is identified by a link, a dom path, and a general regex to match all the similar links"""

	def __init__(self, url, domselector):
		self.url = url
		self.domselector = domselector
		self.regex_pattern = self.patternize(self.url)
	
	@property
	def url(self):
		return self._url

	@url.setter
	def url(self, url):
		from newsline.helpers import helpers
		if not url or url is None: raise Exception("url cannot be empty or None")
		if helpers.is_str(url): 
			if not helpers.is_url(url): 
				raise Exception("url should respect the form a url e.g: http://google.com")
		if helpers.is_list(url):
			if not all(helpers.is_str(u) for u in url):
				raise Exception("url is list, expecting all list elements to be str, however an element (or more) is not")
			elif not helpers.is_url(url):
				raise Exception("url list given, however an element does not respect url pattern. e.g: http://google.com")

		self._url = url

	@property
	def domselector(self):
		return self._domselector

	@domselector.setter
	def domselector(self, ds):
		if not ds or ds is None: raise Exception("domselector cannot be empty or None")
		if not isinstance(ds, str): raise Exception("domselector is expected to be a string, %s given"%type(ds))
		self._domselector = ds

	def patternize(self, urls):
		"""
		This method will extract the regex pattern of the url as to get all similar links.
		"""
		from . import regexr	
		return regexr.RegexrClass().patternize(urls)