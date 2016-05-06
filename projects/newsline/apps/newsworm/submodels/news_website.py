from .abstract_model import AbstractModel
from django.db import models

class NewsWebsite(AbstractModel):
	root_url = models.CharField(max_length=255)

	# A website has many crawled category prototypes
	@property
	def category_prototypes(self):
		"""
		A website has many categories
		"""
		return self.category_prototypes.all()

	@property
	def articles_prototypes(self):
		"""
		A website has many articles
		"""
		return self.article_prototypes.all()
		
	# A website has many crawled categories
	# @property
	# def categories(self):
	# 	"""
	# 	A website has many categories
	# 	"""
	# 	return self.categories.all()

	# @property
	# def articles(self):
	# 	"""
	# 	A website has many articles
	# 	"""
	#     return self.articles.all()