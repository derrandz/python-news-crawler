from __future__ import unicode_literals

from django.db import models


class AbstractModel(models.Model):
	"""This model represents a newsworm model blueprint. This class has been written for DRY purposes.
	"""
	class Meta:
		abstract = True
		app_label = "newsworm"
