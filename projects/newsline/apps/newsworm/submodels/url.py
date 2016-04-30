from django.db import models
from .abstract_model import AbstractModel

class URL(AbstractModel):
	crawled_url = models.CharField(max_length=100)