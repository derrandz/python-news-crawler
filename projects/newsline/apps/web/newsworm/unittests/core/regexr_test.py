import re

from htmldom import htmldom
from django.test import SimpleTestCase
from newsline.functionalities.tests.base_simple_test import BaseSimpleTestCase
from newsline.helpers.colors_class import ColorsClass
from newsline.apps.web.newsworm.core.regexr import RegexrClass

class RegexrTestCase(BaseSimpleTestCase):
	'''
	A test suit for the regexr class.

	'''
	def SpecialCharsTest(self):
		rg = RegexrClass()
		special_chars = ["/", "?", "-"]
		_string = "/hey?you-"

		self.print_info("Trying to return the special characters in %s" % _string)
		rspchars = rg.special_chars(_string)
		if rspchars == special_chars:
			self.print_success("returned %s" % special_chars)
			self.print_success("OK!")
		else:
			self.print_failure("returned %s" % rspchars)
			self.print_failure("FAILED!")

	def splitTest(self):
		regexr = RegexrClass()
		_links = "www.alyaoum24.com/news/sport"
		print("String to be split: %s" % _links)
		split_string = regexr.split(_links)
		assert isinstance(split_string, list)
		print("Results: ")
		print(split_string)

		_links = "maing?#asdokasd/okao_sdka"
		igndel = ["?", "#"]
		print("String to be split: %s with ignored delimieters %s" % (_links, igndel))
		split_string = regexr.split(_links,igndel)
		assert isinstance(split_string, list)
		print("Results: ")
		print(split_string)

	def patternizeTest(self):
		url_example = "/art_et_culture/index.1.html"

		target_url  = ["/faits_divers/index.1.html", 
						"/faits/index.1.html", 
					  	"/faits-divers/index.1.html"
					  ]
		should_not_match_urls  = ["www.dabanit.com","www.dabanit.com/index.1.html",
									
									"faits-divers/index.html",
									"www.hespress.com/something/index.1.html?page=2",
									"www.hespress.com/something?1/index.1.html",
								  	"faits-divers/index.html?page=1",
								  	"/faits-divers/index.html?page=1",
								  	"http://www.hespress.com/something/index.1.html", 
									"www.hespress.com/something/index.1.html",
									"/faits_divers/index.1.html/one"]

		try:
			regexr = RegexrClass(url_example)
		except Exception as e:
			self.print_failure("Test failed with %s" % str(e))
			raise e
		else:
			print("The provided url : %s" % url_example)
			print("The extracted pattern is : %s" % regexr.pattern)

			self.print_info("\nThese tests should all succeed!\n")
			for url in target_url:
				self.print_with_color("YELLOW", "\nMatching for %s" % url)
				if regexr.strongmatch(url):
					self.print_success("\tMatch succeeded!")
				elif regexr.shallowmatch(url):
					self.print_with_color("DARKCYAN", "\t Matched a part of it, but only shallow")
				else:
					self.print_failure("\tMatch failed!")

			self.print_info("\nThese tests should all fail!\n")
			for url in should_not_match_urls:
				self.print_with_color("YELLOW", "\nMatching for %s" % url)
				if regexr.strongmatch(url):
					self.print_success("\tMatch succeeded!")
				elif regexr.shallowmatch(url):
					self.print_with_color("DARKCYAN", "\t Matched a part of it, but only shallow")
				else:
					self.print_failure("\tMatch failed!")


	def test_regexr_split(self):
		regexr = RegexrClass()
		string = '/article/page_2.html?param=1'
		print("String to be split: %s" % string)
		split_string = regexr.split(string)
		assert isinstance(split_string, list)
		print("Results: ")
		print(split_string)
		if len(split_string) == 12:
			test_passed = split_string[0] == "/" \
						and split_string[1] == "article" \
						and split_string[2] == "/" \
						and split_string[3] == "page" \
						and split_string[4] == "_" \
						and split_string[5] == "2" \
						and split_string[6] == "." \
						and split_string[7] == "html" \
						and split_string[8] == "?" \
						and split_string[9] == "param" \
						and split_string[10] == "=" \
						and split_string[11] == "1"

			if test_passed:
				self.print_success("OK!")
			else:
				self.print_failure("Test failed.")

	def test_remove_double_slash(self):
		examples = ["//alink", "//alink//", "/alink/", "alink//", "///link///link"]
		results = ["/alink", "/alink", "/alink", "alink", "/link/link"]

		regexr = RegexrClass()
		rresults = list(map(regexr.remove_double_slash, examples))

		for i, el in enumerate(results):
			self.print_with_color("BOLD", "Arg Supplied: %s, Expected: %s, Result: %s"% (examples[i], el, rresults[i]))
			if el == rresults[i]:
				self.print_success("OK!")
			else:
				self.print_failure("FAILED!")