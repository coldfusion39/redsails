import logging.handlers


class Utilities(object):

	def set_logging(self):
		"""
		Configure the basic logging environment for the application
		"""
		root_logger = logging.getLogger('redSails')
		root_logger.setLevel(logging.INFO)

		log_formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
		file_handler = logging.FileHandler('redSails.log')
		file_handler.setFormatter(log_formatter)
		root_logger.addHandler(file_handler)

		std_formatter = logging.Formatter("\033[1m\033[32m[+]\033[0m %(message)s")
		console_handler = logging.StreamHandler()
		console_handler.setFormatter(std_formatter)
		root_logger.addHandler(console_handler)

		return root_logger


class Banner(object):
	"""
	redSails banner
	"""
	SHOW = """
        @@@@@@@   @@@@@@@@  @@@@@@@              ,/|\,  
        @@@@@@@@  @@@@@@@@  @@@@@@@@           ,/' |\ \,  
        @@!  @@@  @@!       @@!  @@@         ,/'   | |  \  
        !@!  @!@  !@!       !@!  @!@       ,/'     | |   |  
        @!@!!@!   @!!!:!    @!@  !@!     ,/'       |/    |  
        !!@!@!    !!!!!:    !@!  !!!    ,/__SAILS__|-----'
        !!: :!!   !!:       !!:  !!!  ___.....-----''-----/
        :!:  !:!  :!:       :!:  !:!  \    o  o  o  o    / 
        ::~ ~:::~ ~::~::::~ :::: ::~^-^~^`~^~^~`~^~`~^^~^~-^~^
        ~-^~^-`~^~-^~^`^~^-^~^`^~^-~^~-^~^-`~^~-^~^`^~^-^~^`^~
"""
