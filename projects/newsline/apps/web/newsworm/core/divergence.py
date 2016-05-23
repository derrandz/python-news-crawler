def divergent(dvgpoint):
	"""
	If there are no decorator arguments, the function
	to be decorated is passed to the constructor.
	"""
	def class_rebuilder(cls):
		class DivergentClass(cls):
			
			_divergent = True
			_divergence_point = dvgpoint

			def __init__(self, *args, **kws):
				cls.__init__(self, *args, **kws)

			def diverge(self, func):
				func(self)
				_dvattr_name =  self._divergence_point # to avoid confusion
				if hasattr(self, _dvattr_name):
					_dvgattr = getattr(self, _dvattr_name)

					if isinstance(_dvgattr, list):
						for _dvp in _dvgattr:
							func(_dvp)
							_dvp.diverge(func)
					else:
						if isinstance(_dvgattr, cls):
							func(_dvgattr)
							_dvgattr.diverge(func)

		return DivergentClass
	return class_rebuilder