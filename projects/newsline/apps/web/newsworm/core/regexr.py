import re

class RegexrClass:
	""" A class that handles regex operations for our purposes."""
	_regex_digit           = "(\d+)"
	
	_regex_alpha           = "([a-zA-Z_]+)"
	_regex_alpha_ar        = "([\u0621-\u064A\u0660-\u0669_]+)"
	_regex_alpha_arlt      = "([\u0621-\u064A\u0660-\u0669_a-zA-Z]+)"
	
	_regex_alnum           = "([a-zA-Z0-9_]+)"
	_regex_alnum_ar        = "([\u0621-\u064A\u0660-\u0669_][0-9]+)"
	_regex_alnum_arlt      = "([\u0621-\u064A\u0660-\u0669_a-zA-Z_0-9]+)"
	
	_regex_string          = "([^\s?:\]\[#@,\"\'/}{=]+)" # A string signifies any word contaning any character (even arabic) except /?#@=:{},[]
	
	_regex_url_pattern     = "((?:(?:https?:\/\/)|(?:www\.))?[-a-zA-Z0-9@:%._\+~#=]{4,256}\.[a-z]{2,4}(\/|\.|\=|\?|\#|\?|\+|\&|\~)?(?:[-a-zA-Z0-9@:%_\+.~#?&/=]?)+)|(\/(?:[-a-zA-Z0-9@:%_\+.~#?&/=]?)+)"
	_regex_rooturl_pattern = "((?:(?:https?:\/\/)|(?:www\.))?[-a-zA-Z0-9@:%._\+~#=]{4,256}\.[a-z]{2,4}(\/|\.|\=|\?|\#|\?|\+|\&|\~)?(?:[-a-zA-Z0-9@:%_\+.~#?&/=]?)+)"

	def __init__(self, items=[]):
		if items:
			self.items = items
			self.pattern, self.comppattern = self._patternize()

	@property
	def items(self):
		return self._items

	@items.setter
	def items(self, xitems):
		if not xitems or xitems is None : raise Exception("xitems cannot be an empty or None")
		if isinstance(xitems, list) :
			if not xitems : raise Exception("xitems cannot be an empty list")
			if not all(isinstance(i, str) for i in xitems) : raise Exception("xitems must be a list of strings, an element is not string")
		elif not isinstance(xitems, str) : raise Exception(" expects argument to be a string or a list or strings, %s given." % type(xitems))

		if hasattr(self, "_items"):
			self._items = xitems
			self.pattern, self.comppattern = self._patternize()
		else:
			self._items = xitems

	@property
	def pattern(self):
		return self._pattern
	
	@pattern.setter
	def pattern(self, pat):
		self._pattern = pat

	@property
	def comppattern(self):
		return self._comppattern
	
	@comppattern.setter
	def comppattern(self, comppat):
		self._comppattern = comppat

	def smartmatch(self, item):
		if self.strongmatch(item) : return 0
		if self.shallowmatch(item):
			from functools import partial
			from operator import is_not	
			match = list(filter(partial(is_not, ''), re.findall(self.comppattern, item)[0])).pop(0)

			return 1 if match else -1

		return None

	def strongmatch(self, item):
		match = self._match(item)
		return match.group() == item if match is not None else False

	def shallowmatch(self, item):
		return not (not self._match(item).group()) if self._match(item) is not None else False # We use this not not to return the boolean value

	def _match(self, item):
		return self.comppattern.match(item) if isinstance(item, str) else None

	def _patternize(self):
		""" This method will generate a regex to match the likes of the provided string/strings"""
		pat = self._buildpattern(self.items) if not isinstance(self.items, list) else "( %s )" % "|".join(list(map(self._buildpattern, self.items)))
		return [pat, self.compile(pat)]

	def _buildpattern(self, item):
		""" Returns a list of two elements, the string regex pattern and compiled regex pattern """
		item = self.parse_arabic_urls(item) # In case the provided string had utf-8 unreadable arabic characters

		if item.isdigit() : return self._regex_digit
		
		if item.isalpha():
			if self.is_ar(item): return self._regex_alpha_ar
			if self.is_lat(item): return self._regex_alpha

			return self._regex_alpha_arlt

		if item.isalnum():
			if self.is_arabic(item) : return self._regex_alnum_ar
			if self.is_lat(item) : return self._regex_alnum
			
			return self._regex_alnum_arlt

		# If we have reachved over here, this case is when the item is mixed, meaning containing numbers and chars and symbols
		# Here, we will generate a regular expression as that will match the exact form of the item, and also match a general its general form
		# Example : /category-name/article_1.html
		# (/alpha-alpha/alpha_digit.alpha)|(/string/string)
		# This way we will guarantee to match the links that of the nature : /category/article.html or /cat/article
		print("item: %s" % item)
		print("exactpattern: %s" % self._strongpat(item))
		print("generalpattern: %s" % self._shallowpat(item))

		return "(%s)|(%s)" % (self._strongpat(item), self._shallowpat(item))

	def _strongpat(self, _string):
		""" Generates an exact pattern for the provided string in terms of words, digits, special characters, and alphanumerics"""
		if self.contains_spchars(_string): return ''.join([self.__getatompat(part) for part in self.split(_string)])
		return self.__getatompat(_string)

	def _shallowpat(self, _string):
		""" Generates an shallow pattern for the provided string in terms of strings, digits, and symbols like / ? =  #"""
		return self._generalpat(_string, [":", "-", "@", "_"]) # 

	def _generalpat(self, _string, ignored_delimiters):
		""" Generates an shallow pattern for the provided string in terms of strings, digits, and symbols like / ? =  #"""
		if self.contains_spchars(_string):
			return ''.join([self.__getatomstrpat(part) for part in self.split(_string, ignored_delimiters)]) # the list of delimiters is the a list of those to be ignored
		return self.__getatompat(_string)

	def __getatompat(self, atomicstring, use_str_pattern=False):
		""" returns the atomic pattern of the provided string """
		if atomicstring.isdigit() : return self._regex_digit

		if atomicstring.isalpha():
			if self.is_ar(atomicstring) : return self._regex_alpha_ar
			if self.is_lat(atomicstring) : return self._regex_alpha
			return self._regex_alpha_arlt

		if atomicstring.isalnum():
			if self.is_ar(atomicstring) : return self._regex_alnum_ar
			if self.is_lat(atomicstring) : return self._regex_alnum
			return self._regex_alnum_arlt

		if self.is_sym(atomicstring) : return self.escape(atomicstring)

		return None

	def __getatomstrpat(self, atomicstring):
		return self.escape(atomicstring) if self.is_sym(atomicstring) and len(atomicstring) == 1 else self._regex_string

	def split(self, _string, ign_delimiters=None):
		ignore = ign_delimiters is not None
		if ignore :
			if not isinstance(ign_delimiters, list): raise Exception("ign_delimiters should be a list of strings")
			if not all(isinstance(delim, str) for delim in ign_delimiters) : raise Exception("ign_delimiters list expects all elements to str, some aren't")
		
		_string_parts = []
		_buffer       = ""

		for _c in _string:
			not_ignored = not _c in ign_delimiters if ignore else True 
			if self.is_sym(_c) and not_ignored:
				if _buffer != '' : 
					_string_parts.append(_buffer)
					_buffer = ""
				_string_parts.append(_c)
			else:
				_buffer += _c
		
		if _buffer != '': _string_parts.append(_buffer)

		return _string_parts

	def is_sym(self, _string):
		assert isinstance(_string, str)
		return not _string.isdigit() and not _string.isalpha()

	def special_chars(self, _string):
		""" Returns the symbol in the string e.g: / . , _ - ? ! """
		from functools import partial
		from operator import is_not	
		return list(filter(partial(is_not, None), [spchar if self.is_sym(spchar) else None for spchar in _string]))

	def contains_spchars(self, _string):
		""" Indicates whether a string has any special characters of symbols in it"""
		return True if len(self.special_chars(_string)) > 0 else False

	def del_substring(self, _substring, _string):
		return _string.replace(_substring,'')

	def to_lowercase_(name):
		s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
		return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

	def parse_arabic_urls(self, url):
		import urllib.parse
		return urllib.parse.unquote(url)

	def is_charset(self, _str, lang):
		from alphabet_detector import AlphabetDetector
		return AlphabetDetector().only_alphabet_chars(u'%s' % _str, lang)

	def is_ar(self, _str):
		return self.is_charset(_str, 'ARABIC')

	def is_lat(self, _str):
		return self.is_charset(_str, 'LATIN')

	def is_arlat(self, _str):
		return not (self.is_lat(_str) and self.is_ar(_str))

	def compile(self, pattern):
		return re.compile(pattern, re.IGNORECASE|re.DOTALL) if isinstance(pattern, str) else None
	
	def is_url(self, url):
		return True if self.compile(self._regex_url_pattern).match(url) else False

	def is_rooturl(self, url):
		return True if self.compile(self._regex_rooturl_pattern).match(url) else False

	def escape(self, char):
		""" escapes any provided character"""
		return "(\\" + char + ")" if isinstance(char, str) and self.is_sym(char) else None

	def remove_double_slash(self, url):
		urlbuffer = ""
		for i in range(0, len(url)):
			if i < len(url) - 1:
				chars_same     = url[i] == url[i+1]
				chars_slash    = url[i] == "/" or url[i+1] == "/"
				if not chars_same or (chars_same and not chars_slash):
					urlbuffer += url[i]
			else:
				if url[i] != "/":
					urlbuffer += url[i]

		return urlbuffer