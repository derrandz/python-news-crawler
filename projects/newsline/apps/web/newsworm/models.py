from __future__ import unicode_literals

from django.db import models

# Import models in here

from .submodels.website import Website, ConfigFile, FreshestCrawl
from .submodels.article import Article
