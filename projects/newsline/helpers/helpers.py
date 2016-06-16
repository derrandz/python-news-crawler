from newsline.apps.web.newsworm.core.regexr import RegexrClass

def is_list(object):
	return isinstance(object, list)

def is_str(object):
	return isinstance(object, str)

def is_dict(object):
	return isinstance(object, dict)

def is_none(object):
	return object is None

def is_true(object):
	return object == True

def is_url(url, root=False):
	def _is_url(url, root):
		regxr = RegexrClass()
		if not root:
			if regxr.is_url(url):
				return True
			return False
		else:
			if regxr.is_rooturl(url):
				return True
			return False

	if is_list(url):
		if is_empty(url):
			raise ValueError("url list should not be empty")
		if not all(is_str(a) for a in url):
			raise ValueError("url list items should be strings")
		from functools import partial
		mapfunc = partial(_is_url, root=root)
		return all(is_true(a) for a in list(map(mapfunc, url)))
	elif is_str(url):
		return _is_url(url, root)
	else:
		raise ValueError("url is expected to be an str or a list or str, %s given" % type(url))

def is_retype(object):
	import re
	retype = type(re.compile("[a-z]"))
	return isinstance(object, retype)

def has_http_prefix(url):
	regxr = RegexrClass()
	matches = regxr.compile("(http:\/\/)").search(url)
	if matches:
		if matches.group(0) == 'http://':
			return True
	
	return False

def is_empty(object):
	if isinstance(object, list):
		return not len(object) > 0
	elif isinstance(object, str):
		return object == ""

def path_exists(path):
	import os
	return os.path.exists(path)

def isdir(path):
	import os
	return os.path.isdir(path)

def makedir(path):
	import os
	import errno

    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

def file_get_contents(path):
	if path_exists(path):
		file = open(path, 'r')
		filestring = file.read()
		file.close()	
		return filestring
	else:
		raise ValueError("Provided path does not exist\npath : %s" % path)

def parse_json_file(path):
	import json
	with open(path) as jsonfile: return json.load(jsonfile)

def file_put_contents(path, contents):
	file = open(path, 'w+')
	file.write(contents)
	file.close()	
		
def write_json(path, dictionary):
	import json
	with open(path, 'w') as outfile: json.dump(dictionary, outfile, indent=4, sort_keys=True)

def prettify_json_file(path):	
	write_json(path, parse_json_file(path))

def last_element(arglist):
	assert is_list(arglist, list)
	print("%s is list" % arglist)
	lp = len(arglist) - 1
	if lp >= 0:
		return arglist[lp]
	else:
		return None

def get_base_class(derived_class):
	import inspect
	return inspect.getmro(derived_class)[1]

def map_dictionary(func, dictionary, key=None, notroot=False):
	""" loops through a dictionary's value recursively and applies whatever supplied function"""

	if not func or func is None: raise Exception("map_dictionary expects a function, %s given"%type(func))
	if not is_dict(dictionary): 
		if notroot:
			return dictionary
		else:
			raise Exception("map_dictionary expects a dictionary, %s given"%type(dictionary))

	for k, v in dictionary.items():
		if is_dict(v):
			map_dictionary(func, v, key, notroot=True)
		elif is_list(v):
			def _mpdictionary(_dct, _key=key, _func=func):
				return map_dictionary(func=_func, dictionary=_dct, key=_key, notroot=True)
			dictionary[k] = list(map(_mpdictionary, v))
		else:
			if key is not None:
				key_found = False
				if is_list(key):
					if k in key:
						key_found = True
				elif is_str(key):
					if k == key: 
						key_found = True

				if key_found:
					dictionary[k] = func(v)
			else:
				dictionary[k] = func(v)

	return dictionary

def walk_dictionary(dictionary, func):
	func(dictionary)
	for key, item in dictionary.items():
		if isinstance(item, dict):
			walk_dictionary(item, func) 

def indent(times):
	if not times: return ""

	indbuf = ""
	for i in range(0, times):
		indbuf += "\t"

	return indbuf

def printdash(times):
	if not times: return ""

	import math
	dash = ""
	for i in range(0, math.floor(times)):
		dash += "-"

	return dash

def templify(lurl, turl):
	"""
		put %d instead of the leftmost digit in turl
		match against lurl
		if does not match
		repeat for the leftmost-1 digit
	"""

	from newsline.apps.web.newsworm.core.regexr import SpecificRegexr
	def formatd(_str):
		def countd(_str):
			return sum(c.isdigit() for c in _str)

		def _formatd(_str, pos):
			dcount = [0]
			def isdigit_count(c, pos, dcount=dcount):
				if c.isdigit():
					dcount[0] += 1
					if pos == dcount[0]:
						return True
				return False

			return ''.join(["%d" if isdigit_count(c, pos) else c for c in _str])

		return [_formatd(_str, i+1) for i in range(0, countd(_str))]
	
	def unnaturalformatd(furl, surl):
		from os.path import commonprefix as cp
		import urllib.parse as up
		suffix = cp([up.unquote(furl)[::-1], up.unquote(surl)[::-1]])[::-1]
		surlws = surl.replace(suffix, '')
		print("Commonsuffix between %s and %s: %s" % (furl, surl, suffix))
		return surlws + r"%d" + suffix if suffix[0] != "/" else surlws + r"/%d" + suffix

	templates = formatd(turl)

	pat = SpecificRegexr(lurl, ['%d'])

	for tmp in templates:
		if pat.strongmatch(tmp): 
			return tmp

	template = unnaturalformatd(lurl, turl)
	if pat.shallowmatch(template): 
		return template

	return None