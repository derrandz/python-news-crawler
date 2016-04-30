from __future__ import unicode_literals

from django.db import models

class AbstractModel(models.Model):
	abstract = True
	class Meta:
		app_label = "newsworm"