from django.test import SimpleTestCase
from .base_test import BaseSimpleTestCase, ColorsClass
from htmldom import htmldom
from ..core.regexr import RegexrClass
import re

class RegexrTestCase(BaseSimpleTestCase):
	'''
	A test suit for the regexr class.

	'''
	def test_regexr_split_s(self):
		regexr = RegexrClass()
		_links = "www.alyaoum24.com/news/sport"
		print("String to be split: %s" % _links)
		split_string = regexr.split(_links)
		assert isinstance(split_string, list)
		print("Results: ")
		print(split_string)


	def test_regexr_make_pattern(self):
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
									"www.hespress.com/something/index.1.html",]

		regexr = RegexrClass()
		pattern = regexr.make_pattern(url_example, True)
		compiled_pattern = pattern[1]
		print("The provided url : %s" % url_example)
		print("The extracted pattern is : %s" % pattern[0])
		self.print_info("\nThese tests should all succeed!\n")
		for url in target_url:
			self.print_with_color("YELLOW", "\nMatching for %s" % url)
			if compiled_pattern.match(url):
				self.print_success("\tMatch succeeded!")
			else:
				self.print_failure("\tMatch failed!")

		self.print_info("\nThese tests should all fail!\n")
		for url in should_not_match_urls:
			self.print_with_color("YELLOW", "\nMatching for %s" % url)
			if compiled_pattern.match(url):
				self.print_success("\tMatch succeeded!")
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
