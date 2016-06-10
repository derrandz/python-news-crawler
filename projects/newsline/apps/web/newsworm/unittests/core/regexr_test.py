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

	def isUrlTest(self):
		rg = RegexrClass()
		urls = ["/url", "http://www.url.com", "www.url.com", "#"]

		for u in urls:
			if rg.is_url(u): self.print_success("Matched %s" % u)
			else : self.print_failure("Did not match %s" % u)
 
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
		# _links = "/topics/آش-واقع"
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
		def _match(regexr, urls):
			for url in urls:
				self.print_with_color("YELLOW", "\nMatching for %s" % url)
				if regexr.strongmatch(url):
					self.print_success("\tMatches!")
				elif regexr.shallowmatch(url):
					self.print_warning("\t Matched a part of it, but only shallow")
				else:
					self.print_failure("\tDoes not match!")

		def _match_smart(regexr, urls):
			for url in urls:
				self.print_with_color("YELLOW", "\nMatching for %s" % url)
				sm = regexr.smartmatch(url)
				if sm == 0 : self.print_success("\tMatches!")
				elif sm == 1 : self.print_with_color("CYAN", "\tMatched a part of it, but it seems it contain more!")
				elif sm == -1:
					self.print_with_color("DARKCYAN", "\tMatched a part of it, but it seems to contain less!")
				else:
					self.print_failure("\tDoes not match!")

		def _patternize_test(url_examples, matcheables, unmatcheables):
			self.print_seperator()
			try:
				regexr = RegexrClass(url_examples)
			except Exception as e:
				self.print_failure("Test failed with %s" % str(e))
				raise e
			else:
				print("The provided urls : %s" % url_examples)
				print("The extracted pattern is : %s" % regexr.pattern)

				self.print_info("\nThese tests should all succeed!\n")
				_match(regexr, matcheables)

				self.print_info("\nThese tests should all fail!\n")
				_match(regexr, unmatcheables)

			self.print_seperator()

		def _patternize_test_smart(url_examples, matcheables, unmatcheables):
			self.print_seperator()
			try:
				regexr = RegexrClass(url_examples)
			except Exception as e:
				self.print_failure("Test failed with %s" % str(e))
				raise e
			else:
				print("The provided urls : %s" % url_examples)
				print("The extracted pattern is : %s" % regexr.pattern)

				self.print_info("\nThese tests should all succeed!\n")
				_match_smart(regexr,matcheables)

				self.print_info("\nThese tests should all fail!\n")
				_match_smart(regexr, unmatcheables)
			self.print_seperator()

		_patternize_test([
			"/art-et-culture/index.1.html",
			"/politique/index.1.html"
		], 
		[
			"/fait-divers/index.1.html",
			"/fait_divers/index.1.html",
			"/news/index.1.html",
		], 
		[
			"www.dabanite.com",
			"/videos",
			"/news",	
			"/politique/index.1.html/articles"
		])

		_patternize_test(
			"/news?page=1" 
		,[
			"/news-and-articles?page=1",
			"/articles_and_news?page=2",
			"/stuff?page=2"
		], 
		[
			"/what/what",
			"/subscribe/win",
			"/123page"
		])

		_patternize_test(
			"/news/politics?page=1" 
		,[
			"/news/art-et-culture?page=1",
			"/news/articles_and_news?page=2",
			"/news/stuff?page=2"
		], 
		[
			"/what/what",
			"/subscribe/win",
			"/123page"
		])

		_patternize_test(
			"/news/politics" 
		,[
			"/news/art-et-culture",
			"/news/articles_and_news",
			"/news/stuff?page=2"
		], 
		[
			"/news/politics/article1.html",
			"/news",
			"/123page"
		])

		_patternize_test_smart(
			"/news/politics?page=1" 
		,[
			"/news/art-et-culture?page=1",
			"/news/articles_and_news?page=2",
			"/news/stuff?page=2"
		], 
		[
			"/news/sports",
			"/news/sports?page=1#nav_item_tab",
			"/news/sports?page=1/something",
			"/news/sports?page=1/news/sports?page=1",
			"/news"
		])



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
		examples = ["//alink", "//alink//", "/alink/", "alink//", "///link///link", "http://link//linkk", "/link/http://link/link"]
		results = ["/alink", "/alink", "/alink", "alink", "/link/link", "http://link/linkk", "/link/http://link/link"]

		regexr = RegexrClass()
		rresults = list(map(regexr.remove_double_slash, examples))

		for i, el in enumerate(results):
			self.print_with_color("BOLD", "Arg Supplied: %s, Expected: %s, Result: %s"% (examples[i], el, rresults[i]))
			if el == rresults[i]:
				self.print_success("OK!")
			else:
				self.print_failure("FAILED!")


from newsline.apps.web.newsworm.core.regexr import SpecificRegexr
class SpecificRegexrTestCase(BaseSimpleTestCase):

	def testTemplify(self):
		from newsline.helpers.helpers import templify
		expected = '/faits-divers/index.%d.html'
		result = templify('/politique/index.%d.html', '/faits-divers/index.1.html')
		if result == expected:
			self.print_success("Test passed with result: \n%s, \nwas expecting: \n%s" %  (result, expected))
		else:
			self.print_failure("Test failed with result: \n%s \nwhile expecting \n%s" % (result, expected))

	def printPattern(self):
		fd = '/faits-divers/index.%d.html'
		sp = SpecificRegexr(fd, ['%d'])
		self.print_info("Schema for %s: %s" % (fd, sp.pattern))

	def testMatching(self):
		sp = SpecificRegexr('/faits-divers/index.%d.html', ['%d'])

		tagainst = [
			'/politique/index.%d.html',
			'/news/index.%d.html',
			'/something/index.%d.html',
			'/something/index.1.html',
			'/news/index.%d.html/see',
		]

		for el in tagainst:
			if sp.strongmatch(el):
				self.print_success("Matched %s" % el)
			else:
				self.print_failure("Did not match %s" % el)