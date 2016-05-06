from django.test import TestCase

class ColorsClass:
	
	colors = {
		"PURPLE" : '\033[95m',
		'CYAN' : '\033[96m',
		'DARKCYAN' : '\033[36m',
		'BLUE' : '\033[94m',
		'GREEN' : '\033[92m',
		"YELLOW" : '\033[93m',
		"RED" : '\033[91m',
		"BOLD" : '\033[1m',
		"UNDERLINE" : '\033[4m'
	}

	PURPLE    = '\033[95m'
	CYAN      = '\033[96m'
	DARKCYAN  = '\033[36m'
	BLUE      = '\033[94m'
	GREEN     = '\033[92m'
	YELLOW    = '\033[93m'
	RED       = '\033[91m'
	BOLD      = '\033[1m'
	UNDERLINE = '\033[4m'
	END       = '\033[0m'

	@classmethod
	def getcolor(cls, color):
		return cls.colors[color]



class BaseTestCase(TestCase):
	class Meta:
		app_label = "newsworm"
	
	def print_success(self, content):
		print(ColorsClass.BOLD + ColorsClass.GREEN + content + ColorsClass.END)

	def print_failure(self, content):
		print(ColorsClass.BOLD + ColorsClass.RED + content + ColorsClass.END)

	def print_warning(self, content):
		print(ColorsClass.BOLD + ColorsClass.YELLOW + content + ColorsClass.END)

	def print_info(self, content):
		print(ColorsClass.BOLD + ColorsClass.CYAN + content + ColorsClass.END)

	def print_with_bold_color(self, color, content):
		print(ColorsClass.BOLD + ColorsClass.getcolor(color)+ content + ColorsClass.END)

	def print_with_color(self, color, content):
		print(ColorsClass.getcolor(color) + content + ColorsClass.END)


