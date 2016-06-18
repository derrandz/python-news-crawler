from newsline.apps.web.newsworm.core.bloom_filter import WormSimpleBloomFilter
from newsline.functionalities.tests.base_simple_test import BaseSimpleTestCase

class BloomFilterTestCase(BaseSimpleTestCase):

	def testFileCreation(self):
		path = '/home/hrt/Desktop/bloom/bands.bloom'
		try:
			WormSimpleBloomFilter(10, 0.00000001, path)
		except Exception as e:
			self.print_failure("Test failed with: %s" % str(e))
			raise e
		else:
			import os
			if os.path.exists(path):
				self.print_success("File created successfully")
			else:
				self.print_failure("Failed to crate file")

	def testBloomFilter(self):
		items = ['glass', 'moon', 'mouse', 'cat', 'extra', 'pot']

		filepath = '/home/hrt/Desktop/bloom/new2.bloom'
		
		bloomfilter = WormSimpleBloomFilter(len(items), 0.001, filepath)
		
		bloomfilter.add(items)

		nitems = ['Jackson', 'Ford', 'stuff']

		ci = 0
		for i in items:
			if i in bloomfilter:
				self.print_success("%s in bloomfilter" % i)
			else:
				ci += 1
				self.print_warning("%s not in bloomfilter" % i)

		if ci != 0 :
			self.print_failure("\nFirst part of test failed with %d elemented missed" % ci)
		else:
			self.print_success("\nTest passed!, all elements of bloomfilter are found")

		self.print_seperator()

		ci = 0
		for i in nitems:
			if i in bloomfilter:
				ci += 1
				self.print_success("%s in bloomfilter" % i)
			else:
				self.print_warning("%s not in bloomfilter" % i)

		if ci != 0 :
			self.print_failure("\nFirst part of test failed with %d elemented found" % ci)
		else:
			self.print_success("\nTest passed!, all elements that are not in the bloomfilter weren't found")

		print(bloomfilter.bit_array)
		# bloomfilter = WormSimpleBloomFilter(len(items), 0.001, filepath)
		# print("Post reinit")
		# print(bloomfilter.bit_array)


	def testOldBloomFilterFile(self):
		items = ['glass', 'moon', 'mouse', 'cat', 'extra', 'pot']
		nitems = ['Jackson', 'Ford', 'stuff']

		bloomfilter = WormSimpleBloomFilter(len(items), 0.001, '/home/hrt/Desktop/bloom/new2.bloom')

		ci = 0
		for i in items:
			if i in bloomfilter:
				self.print_success("%s in bloomfilter" % i)
			else:
				ci += 1
				self.print_warning("%s not in bloomfilter" % i)

		if ci != 0 :
			self.print_failure("\nFirst part of test failed with %d elemented missed" % ci)
		else:
			self.print_success("\nTest passed!, all elements of bloomfilter are found")

		self.print_seperator()

		ci = 0
		for i in nitems:
			if i in bloomfilter:
				ci += 1
				self.print_success("%s in bloomfilter" % i)
			else:
				self.print_warning("%s not in bloomfilter" % i)

		if ci != 0 :
			self.print_failure("\nFirst part of test failed with %d elemented found" % ci)
		else:
			self.print_success("\nTest passed!, all elements that are not in the bloomfilter weren't found")

		print(bloomfilter.bit_array)
