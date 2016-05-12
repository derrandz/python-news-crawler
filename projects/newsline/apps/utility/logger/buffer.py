import io

class Buffer:
	"""
	This class serves a string buffer
	"""

	def __init__(self):
		self._stringio = io.StringIO()
		self.done = False

	def __str__(self):
		return self._stringio.getvalue()

	def push(self, *objects, sep=' ', end=''):
		if not self.done:
			print(*objects, sep=sep, end=end, file=self._stringio)
		else:
			import warnings
			warnings.warn("Warning:\n\t The pushed data will be dismissed because you are trying to push it to a finished buffer.\n User reinit to use the buffer again.")

	def pushnl(self, *objects):
		self.push(*objects, end='\n')

	def pushind(self, *objects):
		self.push(*objects, end='\n')

	def close(self):
		self.done = True

	def reinit(self):
		self._stringio = io.StringIO()
		self.done = False

class LogFileBuffer(Buffer):
	
	def __init__(self, name):
		Buffer.__init__(self)
		self.name = name
		
	def init(self):
		import datetime
		now  = datetime.datetime.now()
		date = "%i/%i/%i" % (now.month, now.day, now.year)
		time = "[%d:%d]" % (now.hour, now.minute)

		self.pushnl("# %s %s: INIT PUSH, BEGIN" % (date, time))
		return self
	
	def close(self):
		import datetime
		now  = datetime.datetime.now()
		date = "%s/%s/%s" % (now.month, now.day, now.year)
		time = "[%s:%s]" % (now.hour, now.minute)
		
		self.pushnl("# %s %s: FINAL PUSH, FINISH" % (date, time))

		self.done = True
	
	def reinit(self):
		Buffer.reinit(self)
	
