from newsline.apps.newsworm.submodels.news_website import NewsWebsite
from .base_test import BaseTestCase

class ModelsTestCase(BaseTestCase):

	def test_newswebsite_model(self):
		website = NewsWebsite(root_url="http://www.hespress.com")
		try:
			
		if website.save():
			self.print_success("A newswebsite line has been added to the database successful.")
			self.print_success("id: %d, url: %s" % (wehsite.id, website.root_url))
		else:
			self.print_failure("Failed to insert a a newswebsite line to the database")	

	def test_category_prototype_model(self):
		pass

	def test_article_prototype_model(self):
		pass