'''

			  [DESCRIPTION]
		 This file keeps Controller
		class which helps to organizate
		   work with user an errors
	
				[CREATORS]
			 Name: Miasnenko Dmitry
	GitHub: https://github.com/YoungMeatBoy 

'''

import datetime
from colors import *

class Controller(object):
	def __init__(self, print_flag:bool = True, ask_flag:bool = True) -> None:
		self.print_flag = print_flag
		self.ask_flag = ask_flag
		self.assert_printing = print_flag
	
	'''
	@brief Incapsulation of a standard print
	Runs standart print if self.print_flag == True
	'''
	def locked_print(self, *args, **kwargs) -> None:
		if self.print_flag:
			print(*args, **kwargs)
   
	'''
	@brief Exits the programm with messages of error
	@param[in] message message to display
	@param[in] reason reason to display
	@warning Exits the programm!
	'''
	def finish(self, message:str, reason:str=None) -> None:
		self.locked_print(red('\n[EXIT PROGRAM] [WATCH INFO]'))
		self.locked_print(red(f'[MESSAGE] : {message}'))
		if reason:
			self.locked_print(red(f'[REASON]  : {reason}'))
		exit(1)
	
	'''
	@brief Exits the programm with messages of succes
	@param[in] message message to display
	@param[in] reason reason to display
	@warning Exits the programm!
	'''
	def success(self, message:str=None, *args, **kwargs) -> None:
		self.locked_print(green('\n[PROGRAM FINISHED]'))
		if message:
			self.locked_print(green(f'[MESSAGE] : {message}', *args, **kwargs))
		exit()
	
	'''
	@brief Formates current time
	@return str date
	'''
	def current_time(self) -> str:
		res = datetime.datetime.now()
		res = res.strftime("%d %B %Y (%d.%m.%Y) At: %H:%M:%S")
		return res

	'''
	@brief Sets new print flag
	@return None
	'''
	def set_print_flag(self, new_flag:bool) -> None:
		self.print_flag = new_flag

	'''
	@brief Asks user to make a choice to continue
	@warning Exits the programm
	'''
	def ask_to_continue(self) -> bool:
		if self.ask_flag:
			accept = ("y", "yes", "")
			self.locked_print(red("[ANSWER TO CONTINUE] ", end=""))
			try:
				res = input().lower() in accept
			except KeyboardInterrupt:
				res = 0
			if not res:
				self.finish('Moves were not accepted by a user!')
			else:
				self.locked_print()
				return True
		return True
