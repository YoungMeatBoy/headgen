'''

			  [DESCRIPTION]
		 This file keeps KeyParcer
		class which helps to find
			user keys in lines 
	
				[CREATORS]
			 Name: Miasnenko Dmitry
	GitHub: https://github.com/YoungMeatBoy 

'''

#importing builtins
import re
from typing import List

'''
Key parser class
which organisates work
with keys in the line
you do not have to write
your own parser
'''
class KeyParser():
	def __init__(self) -> None:
		# Pattern which matches 
		# such lines:
		# 	any::any
		#   any::any::
		#   any::any::any
		self.pattern = r'\w{1,}[:][:]\w{1,}[:][:]\w{0,}'
		self.cmp_ptrn = re.compile(self.pattern)
	
	'''
	@brief Matches string according to Pattern
	@param[in] line line to be parsed
	@return found matches
	'''
	def __match__(self, line:str) -> List[str]:
		matched = re.findall(self.cmp_ptrn, line)
		return matched

	'''
	@brief Finds all keys in the line
	@param[in] line line to be parsed
	@return List of found keys
	'''
	def find_keys(self, line:str) -> List[dict]:
		res = list()
		matched = self.__match__(line)
		for found in matched:
			found = found.split('::')
			prog, comand, *values = found
			temp_res = {
						'prog'    : prog,
						'command' : comand,
						'values'  : values
						}
			res.append(temp_res)
		return res

	'''
	@brief Removes all found keys from the line
	@param[in] line line to be cleaned
	@return Modified line
	'''
	def remove_keys_from_line(self, line:str) -> str:
		matched = self.__match__(line)
		for found in matched:
			line = line.replace(found, '')
		return line.replace('//', '', 1)
	
	'''
	@brief Find keys of given programm
	@param[in] line line to be parsed
	@param[in] name name of the programm
	@return List of found keys
	'''
	def get_keys_of(self, line:str, name:str, command:str=None) -> List[dict]:
		res = list()
		matched = self.find_keys(line)
		for found in matched:
			if found['prog'] == name:
				if command:
					if command == found['command']:
						res.append(found)
				else:
					res.append(found)
		return res
	'''
	@brief Gets all values from list of keys
	@param[in] keys list of keys
	@return list of values
	'''
	def get_all_values(self, keys:List[dict]) -> List:
		all_values = sum([_['values'] for _ in keys], [])
		return all_values

	'''
	@brief Gets all commands from list of keys
	@param[in] keys  list of keys
	@return list of commands
	'''
	def get_all_commands(self, keys:List[dict]) -> List:
		return [_['command'] for _ in keys]
