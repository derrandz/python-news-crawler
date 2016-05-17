class ColorsClass:
	
	colors = {
		"BLACK"			:	 "\033[0;30m",
		"BLUE"			:	 "\033[0;34m",
		"GREEN"			:	 "\033[0;32m",
		"CYAN"			:	 "\033[0;36m",
		"RED"			:	 "\033[0;31m",
		"PURPLE"		:	 "\033[0;35m",
		"BROWN"			:	 "\033[0;33m",
		"GRAY"			:	 "\033[0;37m",
		"BOLDGRAY"		:	 "\033[1;30m",
		"BOLDBLUE"		:	 "\033[1;34m",
		"BOLDGREEN"		:	 "\033[1;32m",
		"BOLDCYAN"		:	 "\033[1;36m",
		"BOLDRED"		:	 "\033[1;31m",
		"BOLDPURPLE"	:	 "\033[1;35m",
		"BOLDYELLOW"	:	 "\033[1;33m",
		"WHITE"			:	 "\033[1;37m",
		"NORMAL"		:	 "\033[0m"
	}

	@classmethod
	def get(cls, color):
		return cls.getcolor(color)
	
	@classmethod
	def getcolor(cls, color):
		return cls.colors[color]