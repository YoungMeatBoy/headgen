from headgen.helper_visitor import HelperVisitor
from headgen.key_parser import KeyParser
from typing import List
import re

'''
@brief Takes function name from line
@param[in] line line to be parsed
@return str name of the function
'''
def get_function_name(line):
	before_brace = line.split('(')[0]
	name = before_brace.split().pop()
	return name



class MainVisitor(HelperVisitor):
	def __init__(self, controller):
		self.key_parser = KeyParser()
		self.controller = controller
		self.function_pattern = re.compile(r'^\w{1,}\s?\w{1,}\s?[*]?(\w*)[(](void|((.)*\s?[*]\s?(.)*)){0,}[)]\s?{?(.)*$')
		self.include_pattern = re.compile(r'(loc|std)?\s*[:]\s*.*')

	'''
	@brief Checks if line is a function
	@param[in] line line to be parsed
	@return bool
	'''
	def __is_function__(self, line:str) -> bool:
		return re.match(self.function_pattern, line)

	'''
	@brief Checks if line is not ignored
	@param [in] line line to be parsed
	@return bool
	'''
	def __not_ignored__(self, line) -> bool:
		return 'headgen::no_add' not in line
	
	'''
	@brief Gets all functions from file
	@param [in] filename file to be readed
	@return list of functions
	'''
	def get_functions(self, filename:str) -> List[dict]:
		result = list()
		with open(filename, encoding = "utf-8") as opened_file:
			for ind, line in enumerate(opened_file):
				if self.__is_function__(line) and self.__not_ignored__(line):
					name = get_function_name(line)
					info = {
						'name' : name,
						'signature' : self.get_function_signature(line),
						'documentation' : ''
					}
					result.append(info)
		return result

	'''
	@brief links documentation from file with functions
	@param[in]  filename file to be parsed
	@param[in] list of functions
	@return list of functions linked with documentation
	'''
	def get_documentation(self, filename:str, functions:List[dict]):
		with open(filename, encoding = "utf-8") as opened_file:
			for ind, line in enumerate(opened_file):
				keys = self.key_parser.get_keys_of(line, 'headgen', 'link')
				no_keys_line = self.key_parser.remove_keys_from_line(line)
				if keys:
					doc = no_keys_line
					start_comment_line_number = ind
					
					while True:
						try:
							line = next(opened_file)
							if '*/' in line:
								doc += line
								break
							else:
								doc += line
						except StopIteration:
							reason = {
								'message': 'Impossible to find documentation for functions',
								'reason' : f'Unclosed bracket stored at line {start_comment_line_number}'
							}
							self.controller.finish(**reason)
					link_name = self.key_parser.get_all_values(keys).pop()
					
					for func in functions:
						if link_name == func['name']:
							func['documentation'] = doc
		return functions

	def __is_include__(self, line:str):
		return re.match(self.include_pattern, line)
	
	def get_includes(self, filename:str):
		res = list()	
		sort_flag = False
		with open(filename, encoding = "utf-8") as opened_file:
			for line_ind, line in enumerate(opened_file):
				keys_includes = self.key_parser.get_keys_of(line, 'headgen', 'includes')
				keys_sort = self.key_parser.get_keys_of(line, 'headgen', 'sort')
				if keys_includes:
					if keys_sort:
						sort_flag = keys_sort['values'].pop() == 'enable'
					while True:
						try:
							line = next(opened_file)
							if '*/' in line:
								break
							else:
								if self.__is_include__(line):
									typ, name = line.split(':')
									res.append({'type' : typ.strip(), 
												'headername' : name.strip()
												})
						except StopIteration:
							reason = {
									'message' : 'Impossible to create header!',
									'reason'  : f'Could not read includes as comment at line {line_ind} is not closed!'
								}
							self.controller.finish(**reason)
		return res, sort_flag

	def get_defines(self, file:str):
		before = list()
		after = list()
		with open(file, 'r', encoding = "utf-8") as opened_file:
			for line in opened_file:
				if '#define' in line:
					add_flag = not self.key_parser.get_keys_of(line, 'headgen', 'no_add')
					no_keys_line = self.key_parser.remove_keys_from_line(line).strip().lstrip('//')
					if add_flag:
						place_setted = self.key_parser.get_keys_of(line, 'headgen', 'place_before')
						if place_setted and place_setted['values'] and 'includes' in place_setted['values']:
							before.append(no_keys_line)
						else:
							after.append(no_keys_line)
		return before, after

	def get_enums(self, file):
		res = []
		with open(file, 'r', encoding = "utf-8") as opened_file:
			for ind, line in enumerate(opened_file):
				watch = self.key_parser.get_keys_of(line, 'headgen', 'watch')
				line_num = ind
				if watch:
					watch = watch.pop()
					if 'enum' in watch['values']:
						en = ''
						while True:
							try:
								line = next(opened_file)
								if '*/' in line:
									break
								else:
									en += line
							except StopIteration:
								reason = {
									'message' : 'Impossible to create header!',
									'reason'  : f'Comment on line {line_num} is not closed!'
								}
								self.controller.finish(**reason)
						res.append(en)
		return res

	def get_structures(self, file):
		res = []
		with open(file, 'r', encoding = "utf-8") as opened_file:
			for ind, line in enumerate(opened_file):
				watch = self.key_parser.get_keys_of(line, 'headgen', 'watch')
				line_num = ind
				if watch:
					watch = watch.pop()
					if 'struct' in watch['values']:
						st = ''
						while True:
							try:
								line = next(opened_file)
								if '*/' in line:
									break
								else:
									st += line
							except StopIteration:
								reason = {
									'message' : 'Impossible to create header!',
									'reason'  : f'Comment on line {line_num} is not closed!'
								}
								self.controller.finish(**reason)
						res.append(st)
		return res


	def test_function_regexp(self, files):
		for file in files:
			print(f"TESTING : {file}")
			with open(file, 'r', encoding = "utf-8") as opened_file:
				for line in opened_file:
					if re.match(self.function_pattern, line):
							print(f"MATCHED: {line}")