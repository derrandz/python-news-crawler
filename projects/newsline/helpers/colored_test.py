from .colors_class import ColorsClass

class ColoredTest:

	def print_success(self, content):
		print(ColorsClass.get("BOLD") + ColorsClass.get("GREEN") + content + ColorsClass.get("END"))

	def print_failure(self, content):
		print(ColorsClass.get("BOLD") + ColorsClass.get("RED") + content + ColorsClass.get("END"))

	def print_warning(self, content):
		print(ColorsClass.get("BOLD") + ColorsClass.get("YELLOW") + content + ColorsClass.get("END"))

	def print_info(self, content):
		print(ColorsClass.get("BOLD") + ColorsClass.get("CYAN") + content + ColorsClass.get("END"))

	def print_with_bold_color(self, color, content):
		print(ColorsClass.get("BOLD") + ColorsClass.getcolor(color)+ content + ColorsClass.get("END"))

	def print_with_color(self, color, content):
		print(ColorsClass.getcolor(color) + content + ColorsClass.get("END"))


