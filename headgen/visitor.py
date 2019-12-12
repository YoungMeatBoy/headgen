from headgen.helper_visitor import HelperVisitor
from headgen.key_parser import KeyParser
from pycparser import c_ast
from typing import List
import re

def get_function_name(func):
	return ''.join(func.split('(')[0]).split().pop()

class MainVisitor(c_ast.NodeVisitor, HelperVisitor):

	def __init__(self, controller):
		self.key_parser = KeyParser()
		self.controller = controller

	def get_functions(self, filename):
		self.cache_functions = []
		pt = re.compile(r'\w{0,}\s?\w{0,}\s?[*]?(\w.*)[(](.*)[)]\s?{?')
		with open(filename, 'r') as f:
			for ind, line in enumerate(f):
				if re.match(pt, line):
					name = get_function_name(line)
					self.cache_functions.append({'name' : name, 'coordinates' : {'line' : ind + 1, 'start' : 0}, 'documentation' : '', 'line' : line})
			
		for function in self.cache_functions:
			line = function['line']
			if 'headgen::no_add' in line:
				self.cache_functions.remove(function)
			function['signature'] = self.get_function_signature(line)
		return self.cache_functions

	def get_documentation(self, file, functions):
		with open(file, 'r') as opened_file:
			for ind, line in enumerate(opened_file):
				if '/*' in line:
					doc = ''
					start_comment_line_number = ind
					count_closing_brackets = 0
					keys = self.key_parser.get_keys_of(line, 'headgen')
					doc += self.key_parser.remove_keys_from_line(line)
					while True:
						try:
							line = next(opened_file)
						except StopIteration:
							reason = {
								'message': 'Impossible to find documentation fo functions',
								'reason' : f'Unclosed bracket stored at line {start_comment_line_number}'
							}
							self.controller.finish(**reason)
						else:
							doc += line
							if '*/' in line:
								if count_closing_brackets:
									count_closing_brackets -= 1	
								else:
									break
							elif '/*' in line:
								count_closing_brackets += 1
					if keys:
						link = keys[0]['values'][0]
					else:
						link = ''
					for func in functions:
						if link == func['name']:
							func['documentation'] = doc

	def get_includes(self, file:str):
		res = []	
		sort_flag:bool = False
		with open(file, 'r') as opened_file:
			for line_ind, line in enumerate(opened_file):
				keys = self.key_parser.get_keys_of(line, 'headgen')
				if keys:
					if 'includes' in [_['command'] for _ in keys]:
						sort_flag = 'enable' in sum([com['values'] for com in keys], [])
						while True:
							try:
								line = next(opened_file)
							except StopIteration:
								reason = {
											'message' : 'Impossible to create header!',
											'reason'  : f'Could not read includes as comment at line {line_ind} is not closed!'
										}
								self.controller.finish(**reason)
							else:
								if '*/' in line:
									break
								else:
									if 'loc' in line or 'std' in line:
										typ, name = line.split(':')
										res.append({'type' : typ, 'headername' : name.strip()})
		return res, sort_flag

	def get_defines(self, file:str):
		before = list()
		after = list()
		with open(file, 'r') as opened_file:
			for line in opened_file:
				if '#define' in line:
					keys = self.key_parser.get_keys_of(line, 'headgen')
					if keys:
						if 'no_add' not in [_['command'] for _ in keys]:
							if 'includes' in sum([_['values'] for _ in keys], []):
								before.append(self.key_parser.remove_keys_from_line(line).strip())
							else:
								after.append(self.key_parser.remove_keys_from_line(line).line.strip())
					else:
						after.append(self.key_parser.remove_keys_from_line(line).strip())
		return before, after

	def get_enums(self, file):
		res = []
		with open(file, 'r') as opened_file:
			for ind, line in enumerate(opened_file):
				keys = self.key_parser.get_keys_of(line, 'headgen')
				all_commands = self.key_parser.get_all_commands(keys)
				all_values = self.key_parser.get_all_values(keys)
				line_num = ind
				if 'watch' in all_commands:
					if 'enum' in all_values:
						en = ''
						while True:
							try:
								line = next(opened_file)
							except StopIteration:
								reason = {
									'message' : 'Impossible to create header!',
									'reason'  : f'Comment on line {line_num} is nt closed!'
								}
								self.controller.finish(**reason)
							else:
								if '*/' in line:
									break
								else:
									en += line
						res.append(en)
		return res

	def get_structures(self, file):
		res = []
		with open(file, 'r') as opened_file:
			for ind, line in enumerate(opened_file):
				keys = self.key_parser.get_keys_of(line, 'headgen')
				all_commands = self.key_parser.get_all_commands(keys)
				all_values = self.key_parser.get_all_values(keys)
				line_num = ind
				if 'watch' in all_commands:
					if 'struct' in all_values:
						en = ''
						while True:
							try:
								line = next(opened_file)
							except StopIteration:
								reason = {
									'message' : 'Impossible to create header!',
									'reason'  : f'Comment on line {line_num} is nt closed!'
								}
								self.controller.finish(**reason)
							else:
								if '*/' in line:
									break
								else:
									en += line
						res.append(en)
		return res