import datetime

from .buffer import LogFileBuffer
from newsline.helpers import helpers

class LogSession:
	"""
	This is a complementary class for the logger class.
	A log session can have one or multiple log files, and each program or class that might log will have one session.

	"""
	def __formatdate(self):
		now = datetime.datetime.now()
		return "%s%s%s" % (now.month, now.day, now.year)

	def __formattime(self):
		now = datetime.datetime.now()
		return "%s%s" % (now.hour, now.minute)

	def __format_filename(self):
		return "%s_%s_%s_%i" % (self.__formatdate(), self.__formattime(), self.name, len(self.logfiles))
		
	def __format_directoryname(self):
		from django.conf import settings
		return settings.LOG_FILES_STORAGE + "/" + "%s_%s_log_session" % (self.__formatdate(), self.name)

	def bootstrap_directory(self):
		import os
		directory = self.__format_directoryname()
		self.directory = directory
		if not os.path.exists(directory):
			os.makedirs(directory)

	def bootstrap_active_logfile(self):
		self.active_logfile = {"name": self.__format_filename(), "is_finished": False, "active": True}

	def forget_active_logfile(self):
		self.active_logfile = {"name": "", "is_finished": "", "active": ""}

	def write_active_logfile(self):
		from newsline.helpers import helpers
		helpers.file_put_contents(self.active_file_path, str(self.buffer))

	def commit_active_logfile(self):
		self.active_logfile["active"]      = False
		self.active_logfile["is_finished"] = False
		self.write_active_logfile()
		self.logfiles.append(self.active_logfile)
		self.forget_active_logfile()

	def close(self):
		self.buffer.close()

	def log(self, data, newline=True, indent=False):
		data = "\n######## " + data
		if not indent and newline:
			self.buffer.pushnl(data)
		elif indent and not newline:
			self.buffer.pushind(data)
		elif indent and newline:
			self.buffer.pushnl("\t"+data)
		elif not ident and not newline:
			self.buffer.push(data)


	def __init__(self, name):
		self.name           = name
		self.buffer         = LogFileBuffer(self.name)
		self.logfiles       = []
		self.active_logfile = {}
		self.directory      = ''

	def init_session(self):
		self.bootstrap_active_logfile()
		self.buffer.init()
		return self

	def start_logging_session(self):
		self.init_session().bootstrap_directory()
		return self

	def commit_logging_session(self):
		self.commit_active_logfile()
		return self

	def close_logging_session(self):
		self.close()
		self.commit_active_logfile()
		return None

	def abandon_logging_session(self):
		self.forget_active_logfile()
		self.buffer.reinit()
		return self

	@property
	def active_file_path(self):
		path = ""
		if self.directory_name != "" :
			path = self.directory_name + "/"
			if self.active_logfile_name != "" :
				path += self.active_logfile_name
			else:
				raise ValueError("active_logfile_name is empty!")
		else:
			raise ValueError("directory_name is empty!")

		return path				
	
	@property
	def directory_name(self):
		return self.directory

	@property
	def active_logfile_name(self):
		if self.active_logfile["name"] != "":
			return self.active_logfile["name"]
		else:
			import newsline.helpers.helpers as helpers
			return helpers.last_element(self.logfiles)["name"]

	@property
	def directory_path(self):
		from django.conf import settings
		return settings.LOG_FILES_STORAGE + "/" + self.directory_name
	
	@property
	def active_logfile_path(self):
		from django.conf import settings
		return settings.LOG_FILES_STORAGE + "/" + self.directory_name + "/" + self.active_logfile_name

class Logger:
	"""
	This class serves a logger, pushs logs to a buffer that writes to a logfile later on.
	"""
	def __init__(self):
		self.sessions = {} # This dictionary will contain "logging_class" => [list of sessions]

	def register_class(self, logging_class):
		self.sessions.update({logging_class: [
			LogSession(logging_class).start_logging_session()
		]})
		
		from newsline.helpers import helpers
		active_session = helpers.last_element(self.sessions[logging_class])
		if active_session is not None:
			return active_session
		else:
			raise ValueError("LoggerError: Could not register class for logging.")

class LoggerResolver:

	loggerSingleton = Logger()

	@classmethod
	def initLogger(cls):
		if cls.loggerSingleton is None:
			cls.loggerSingleton = Logger()
		else:
			if not isinstance(cls.loggerSingleton, Logger):
				cls.loggerSingleton = Logger()


	@classmethod
	def init_and_bind_logger(cls):
		if cls.loggerSingleton is None:
			cls.initLogger()
			return cls.loggerSingleton
		else: # Force check
			return cls.loggerSingleton

	@classmethod
	def resolve_logger(cls):
		return cls.loggerSingleton if cls.loggerSingleton is not None else cls.init_and_bind_logger()