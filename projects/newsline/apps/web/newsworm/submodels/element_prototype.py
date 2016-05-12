from .abstract_model import AbstractModel
from .news_website import NewsWebsite
from django.db import models
from ..helpers.string_helpers import to_lowercase_

class ElementPrototype(AbstractModel):
	"""
	This class describes any element on the page that might be identifiable by an a element and reachable by a dom path
	With this class, concrete inheritance is implemented.
	"""
	url = models.CharField(max_length=255)
	regex = models.CharField(max_length=255)
	dom_path = models.CharField(max_length=255)
	parent_website = models.ForeignKey(NewsWebsite, on_delete=models.CASCADE, related_name="%(class)s")

	class Meta:
		abstract = True 
