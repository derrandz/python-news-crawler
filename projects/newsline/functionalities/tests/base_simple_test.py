from django.test import SimpleTestCase
from newsline.helpers.colored_test import ColoredTest

class BaseSimpleTestCase(SimpleTestCase, ColoredTest):
	def print_seperator(self):
		self.print_with_bold_color("YELLOW","\n\n--------------------------------------------------------------------------------\n\n")

	def print_exception(self, e):
		self.print_failure("Test failed with error: %s" % str(e))
