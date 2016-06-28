from __future__ import unicode_literals

from django.db import models


class ANewswormModel(models.Model):
	"""This model represents a newsworm model blueprint. This class has been written for DRY purposes.
	"""
	class Meta:
		app_label = 'newsworm'
		abstract = True
		managed = True
