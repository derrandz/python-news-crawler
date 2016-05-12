from newsline.functionalities.tests.base_simple_test import BaseSimpleTestCase

class LoggerTestCase(BaseSimpleTestCase):

	def testLoggerResolving(self):
		from django.conf import settings
		logSession = settings.LOGGER.register_class("LoggerTestCase")
		logSession.log("Testing...")
		logSession.close_logging_session()
		
		directory_path = logSession.directory_path

		from newsline.helpers import helpers
		if helpers.path_exists(directory_path) and helpers.isdir(directory_path):
			self.print_success("Directory %s has been created successfully" % logSession.directory_name)
		
			logSession.commit_active_logfile()
		
			if helpers.path_exists(logSession.active_logfile_path):
				self.print_success("Log file %s has been successfully created" % logSession.active_logfile_name)
			else:
				self.print_failure("Failed to create log file %s" % logSession.active_logfile_name)
		
		else:
			self.print_failure("Failed to create log session directory %s : DIRECTORY ALREADY EXISTS\n\nProceeding to creating the file" % logSession.directory_name)
