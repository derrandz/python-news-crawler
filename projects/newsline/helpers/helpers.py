from newsline.apps.web.newsworm.core.regexr import RegexrClass

def is_list(object):
	return isinstance(object, list)

def is_str(object):
	return isinstance(object, str)

def is_none(object):
	return object is None

def is_url(url):
	regxr = RegexrClass()
	if regxr.compile(regxr._regex_url_pattern).match(url):
		return True
	return False

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
		raise ValueError("Provided path does not exist")

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

def last_element(_list):
	assert(_list, list)
	lp = len(_list) - 1
	if lp >= 0:
		return _list[lp]
	else:
		return None

