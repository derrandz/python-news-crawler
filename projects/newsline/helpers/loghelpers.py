# This file is a helpers functions file for the logging tools


def getLogger(class):
	from django.conf import settings
	return settings.LOGGER.register_class(class)