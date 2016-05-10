from .regexr import RegexrClass

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

def is_empty(object):
	if isinstance(object, list):
		return not len(object) > 0
	elif isinstance(object, str):
		return object == ""

def file_get_contents(path):
	file = open(path, 'r')
	json_string = file.read()
	file.close()	
	return json_string

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