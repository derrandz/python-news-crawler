from django.test import TestCase
from .colored_test import ColoredTest

class BaseTestCase(TestCase, ColoredTest):
	pass

