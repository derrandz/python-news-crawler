from django.test import SimpleTestCase
from newsline.helpers.colored_test import ColoredTest

class BaseSimpleTestCase(SimpleTestCase, ColoredTest):
	pass


