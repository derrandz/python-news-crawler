import re

class RegexrClass:
	"""
	A class that handles regex operations for our purposes.
	"""
	_regex_digit_only  = "(\\d+)"
	_regex_alphanum    = "((?:[a-z][a-z]*[0-9]+[a-z0-9]*))"
	_regex_alpha_only  = "((?:[a-z][a-z]+))"
	_regex_word        = "((?:\w+))"
	_regex_string      = "((?:[^?:#/=0-9])+)" # A string signifies any word contaning any character except /?#
	_regex_url_pattern = "((http|https)\:\/\/)(||www)[a-zA-Z0-9\-\.]+\.[a-zA-Z]{2,3}(\/\S*)?"
	
	def compile(self, pattern):
		return re.compile(pattern, re.IGNORECASE|re.DOTALL)
			
	def escape(self, char):
		"""
		escapes any provided character
		"""
		return "(\\" + char + ")"

	def make_exact_pattern(self, _string):
		"""
		Generates the exact provided pattern in terms of words, digits, special characters, and alphanumerics
		"""
		if self.contains_spchars(_string):
			pattern = ""
			string_split = self.split(_string)

			for part in string_split:
				if part.isdigit():
					pattern += self._regex_digit_only
				elif part.isalpha():
					pattern += self._regex_alpha_only
				elif part.isalnum():
					pattern += self._regex_alphanum
				else:
					pattern += self.escape(part)

			return pattern
		else:
			if _string.isdigit():
				return self._regex_digit_only
			elif _string.isalpha():
				return self._regex_alpha_only
			elif _string.isalnum():
				return self._regex_alphanum

		return None;

	def make_general_pattern(self, _string):
		"""
		Generates a general regex pattern for the provided string in terms of strings, digits, / ? = . #
		"""
		if self.contains_spchars(_string):
			pattern = ""
			delimiters =  [":","/", "?", "=", ".", "#"]
			string_split = self.split(_string, delimiters)

			for part in string_split:
				if part.isdigit():
					pattern += self._regex_digit_only
				else:
					is_delim = False

					for delim in delimiters:
						if part == delim:
							pattern += self.escape(part)
							is_delim = True

					if not is_delim:
						pattern += self._regex_string

			return pattern
		else:
			if _string.isdigit():
				return self._regex_digit_only
			elif _string.isalpha():
				return self._regex_alpha_only
			elif _string.isalnum():
				return self._regex_alphanum

		return None;

	def make_pattern(self, string, noslash=None):
		"""
		Makes a pattern
		"""
		_noslash = False
		if noslash is not None:
			_noslash = noslash

		if string == '' :
			return [None, None]
		elif string.isalpha():
			return [self._regex_word, re.compile(self._regex_word)]
		elif string.isdigit():
			return [self._regex_digit_only, re.compile(self._regex_digit_only)]
		elif string.isalnum():
			return [self._regex_alphanum, re.compile(self._regex_alphanum)]
		else: # This case is when the string contains any kind of symbols

			# In this sectiion, we will provide a regular expression as follows:
			# An exact regular expression to match all the likes of this string
			# and a general one.
			# Example : /category-name/article_1.html
			# (slash word dash word slash word underscore digit dot word)|(slash string slash word digit word)
			gpattern = "(" + self.make_exact_pattern(string) + ")|(" + self.make_general_pattern(string) + ")"
			return [gpattern, re.compile(gpattern, re.IGNORECASE|re.DOTALL)]

	def _regexr_word_spchars(self, spchars, noslash=None):
		# ((?:\w*((\spchar_1)|(\spchar_2)|(\spchar_3)))*\w+)
		gpattern = ""
		if len(spchars) > 1:
			pattern = "((?:\w*("
			for i, spchar in enumerate(spchars):
				if noslash is not None:
					if noslash:
						if spchar != "/" :
							if i == len(spchars) - 1:
								pattern += "(\\" + spchar + "))"
							else:
								pattern += "(\\" + spchar + ")|"
					else:
						if i == len(spchars) - 1:
							pattern += "(\\" + spchar + "))"
						else:
							pattern += "(\\" + spchar + ")|"

			pattern += ")*\w+)"
			gpattern = pattern
		else:
			pattern = '((?:\w*\\' + spchars[0] +')*\w+)'
			gpattern = pattern

		return gpattern


	def split(self, _string, delimiters=None):
		split_string   = []
		word_container = ""
		for _c in _string:
			is_sym = (not _c.isdigit()) and (not _c.isalpha()) 

			is_del = True
			if delimiters is not None:
				assert isinstance(delimiters, list)
				_is_del = 0
				for delim in delimiters:
					if _c != delim:
						_is_del += 1

				if _is_del == len(delimiters):
					is_del = False

			if is_sym and is_del:
				if word_container != '' : 
					split_string.append(word_container)
					word_container = ""
				split_string.append(_c)
			else:
				word_container += _c

		
		if word_container != '':
			split_string.append(word_container)

		return split_string


	def contains_spchars(self, _string):
		if len(self.special_chars(_string)) > 0:
			return True
		else:
			return False


	def special_chars(self, _string):
		"""
		Returns the symbol in the string e.g: / . , _ - ? ! 
		"""

		spchars = []
		for char in _string:
			if char.isdigit(): 
				pass
			elif not char.isalpha(): 
				spchars.append(char)

		return spchars

	def del_substring(self, _substring, _string):
		return _string.replace(_substring,'')

	def to_lowercase_(name):
		s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
		return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()