from django.test import SimpleTestCase
from .colored_test import ColoredTest

class BaseSimpleTestCase(SimpleTestCase, ColoredTest):
	pass


