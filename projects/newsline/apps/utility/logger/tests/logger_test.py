import re

from django.test import SimpleTestCase
from newsline.functionalities.tests.base_simple_test import BaseSimpleTestCase

from newsline.apps.utility.logger.core import logger

class LoggerTestCase(BaseSimpleTestCase):

	@logger.log_class
	class TestCaseClass(logger.WorkflowStep):

		log_directory_name = "testcaseclass_logs"
		log_name = "TestCaseClass"
		
		@logger.log_method
		def TestCaseMethod(self, a, b):
			self.log("Received arg a: %i"%a)
			self.log("Received arg b: %i"%b)

			self.log("Returning a + b: %i + %i" % (a, b))
			return a + b


	def hello_world(self):

		LogTestCase = self.TestCaseClass()
		LogTestCase.TestCaseMethod(7, 2)
		LogTestCase.close_logging_session()