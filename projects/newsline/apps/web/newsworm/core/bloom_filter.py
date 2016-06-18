import mmh3
import math
from bitarray import bitarray

def ln(x): return math.log(x, math.e)

class WormSimpleBloomFilter:
	def __init__(self, items_count, error_rate=0.0001, filename=None, hash_count=None):
		self.size = self.calcsize(items_count, error_rate)
		self.hash_count = hash_count if hash_count is not None else self.calchash(items_count)
		self.filename = filename

	def calcsize(self, n, p):
		return - math.ceil( (n * ln(p)) / math.sqrt(ln(2)))

	def calchash(self, n):
		return math.floor((self.size / n) * ln(2))

	@property
	def size(self):
		return self._size

	@size.setter
	def size(self, s):
		if not isinstance(s, int):
			raise ValueError("Expecting size to be int or long, %s given" % type(s))

		self._size = s

	@property
	def bit_array(self):
		return self._bit_array

	@bit_array.setter
	def bit_array(self, ba):
		self._bit_array = ba
	
	def bit_array_init(self, nosize=False):
		if not nosize:
			self.bit_array = bitarray(self.size)
			self.bit_array.setall(0)
		else:
			self.bit_array = bitarray()

	@property
	def filename(self):
		return self._filename
	
	@filename.setter
	def filename(self, fn):
		if fn is not None:
			import os
			if os.path.exists(fn):
				with open(fn,'rb') as f: 
					self.bit_array_init(nosize=True)
					self.bit_array.fromfile(f)

			else:
				self.bit_array_init()
				self._update_file(fn)

		self._filename = fn

	def add(self, elements):
		if isinstance(elements, list):
			for el in elements: self._add(el)
		else:
			self._add(elements)

		self._update_file(self.filename)

	def _update_file(self, filename):
		if filename is not None: 
			with open(filename, 'wb') as f: self.bit_array.tofile(f)

	def _hash(self, element):
		return [b % self.size for b in [mmh3.hash(element, i) for i in range(self.hash_count)]]

	def __contains__(self, element):
		return True if all(self.bit_array[b] == 1 for b in self._hash(element)) else False

	def _add(self, el):
		for el in self._hash(el): self.bit_array[el] = 1