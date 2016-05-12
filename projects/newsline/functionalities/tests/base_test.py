from django.test import TestCase
from newsline.helpers.colored_test import ColoredTest

class BaseTestCase(TestCase, ColoredTest):
	pass

