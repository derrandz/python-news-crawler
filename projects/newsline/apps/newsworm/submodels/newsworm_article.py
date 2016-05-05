# 
# 
# 
from django.db import models
from .abstract_model import AbstractModel

class NewswormArticle(AbstractModel):
	'''
		This class will represent the crawled articles that will be put into the database.
	'''

	# Attributes
	crawled_url = models.CharField(max_length=100)

	# Methodes
	def __init__(self, param):
		self.param = param

	def method(self):
		'Simple method'