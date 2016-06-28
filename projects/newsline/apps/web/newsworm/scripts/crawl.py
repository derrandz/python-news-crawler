def fun():
	pass

def run():
	from django.conf import settings
	from newsline.apps.web.newsworm.models import Website
	from newsline.apps.web.newsworm.policies.crawls import InitialCrawl

	url = "http://hespress.com"
	website = Website(url=url, name="hespress", configuration_file="%s/data/configurations/hespress.json" % settings.NEWSWORM_DIR)
	website.save()

	crawl = InitialCrawl(url)

	crawl.run()

	print("\n\n\nDone.")	