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

def file_get_contents(path):
	if path_exists(path):
		file = open(path, 'r')
		json_string = file.read()
		file.close()	
		return json_string
	else:
		raise ValueError("Provided path does not exist\npath : %s" % path)

def parse_json_file(path):
	import json
	return json.loads(file_get_contents(path))

def file_put_contents(path, contents):
	file = open(path, 'w')
	file.write(contents)
	file.close()	
		
def write_json(path, dictionary):
	import json
	file_put_contents(path, json.dumps(dictionary, indent=4, sort_keys=True))

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