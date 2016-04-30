from __future__ import unicode_literals

from django.db import models

class AbstractModel(models.Model):
	class Meta:
		app_label = "newsworm"
		abstract = True