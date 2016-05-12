from .colors_class import ColorsClass

class ColoredTest:

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


