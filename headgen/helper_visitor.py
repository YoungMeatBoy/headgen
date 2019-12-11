'''

			  [DESCRIPTION]
		 This file keeps classes
		which help MainVisiror to
			  parce c_ast.

				[CREATORS]
			 Name: Miasnenko Dmitry
	GitHub: https://github.com/YoungMeatBoy 

'''

# built in modules
import os
import re
from itertools import islice
from pycparser import c_ast, parse_file
from typing import List


'''
This class takes delegations from
MainVisitoir. It keeps help 
functions. No need to store 
them in MainVisitoir
'''
class HelperVisitor(object):
	'''
	@brief Gets line number from a string
	@param[in] line str line to be checked
	@return int line number
	'''
	def get_line_number_from_string(self, line:str, *args, **kwargs) -> int:
		splited = str(line).split(':')
		start = splited.pop()
		line_number = splited.pop()
		return {'line': int(line_number), 'start' : int(start)}
		 
	'''
	@brief Gets line from a file
	@param[in] filename name of the file
	@param[in] line_number line number
	@warning line is not stripped
	'''
	def get_line_from_file(self, filename:str, line:int, *args, **kwargs) -> str:
		# Checking line index.
		line_index = line - 1
		with open(filename, 'r') as file:
			found_line = list(islice(file, line_index, line))
			try:
				return found_line.pop()
			except:
				return ''

	'''
	@brief Coomments all includes in the file
	@param[in] filename name of the file
	'''
	@staticmethod
	def comment_all_includes(filename:str):
		import fileinput
		with fileinput.FileInput(filename, inplace=True, backup='.bak') as file:
			for line in file:
				line = line.rstrip()  # remove trailing (invisible) space
				splitted = list(line.split("#include"))
				res = "//->temp#include".join(splitted)
				print(res)  # stdout is redirected to the file
		os.unlink(filename + '.bak') # remove the backup on success

	'''
	@brief Uncomments all includes in the file
	@param[in] filename name of the file
	'''
	@staticmethod
	def uncomment_all_includes(filename:str):
		import fileinput
		with fileinput.FileInput(filename, inplace=True, backup='.bak') as file:
			for line in file:
				line = line.rstrip()  # remove trailing (invisible) space
				splitted = list(line.split("//->temp#include"))
				res = "#include".join(splitted)
				print(res)  # stdout is redirected to the file
		os.unlink(filename + '.bak') # remove the backup on success
	
	'''
	@brief GEts ast of the file
	@param[in] filename name of the file
	'''
	def get_ast(self, filename:str):
		self.comment_all_includes(filename)
		try:	
			ast = parse_file(filename,  use_cpp=True,
					cpp_path='gcc',
					cpp_args=['-E', r'-Iutils/fake_libc_include'])
		except:
			self.uncomment_all_includes(filename)
			exit()
		else:
			self.uncomment_all_includes(filename)
		return ast

	'''
	@brief Makes function signature
	@param[in] line dirty line with signatre
	@return str signature
	'''
	def get_function_signature(self, line:str) -> str:	
		return line.strip().split('{')[0].strip() + ';\n'

	'''
	@brief Prettify includes
	@param[in] includes list of found includes
	'''
	def prettify_includes(self, includes:List[str], sorting:bool=False) -> List[str]:
		res = list()
		for inc in includes:
			headername = inc['headername']
			if inc['type'] == 'std':
				res.append(f'#include <{headername}>')
			elif inc['type'] == 'loc': 
				res.append(f'#include "{headername}"')
		if sorting:
			buildins = [_ for _ in res if '<' in _]
			local = [_ for _ in res if '"' in _]
			buildins = sorted(buildins)
			local = sorted(local)
			res = buildins + local
		return res

			
	 
'''
Handles nodes wich
were given to MainVisitor
Using this we clean logic
of MainVisitor class
'''
class Handler(HelperVisitor):
	def __init__(self) -> None:	
		#Initing HelperVisitor
		self.__super__.__init__()
	
	'''
	@brief Handles function node
	@param[in] node type FuncDef
	@return function info
	'''
	def handle_function(self, node, *args, **kwargs):
		name = node.decl.name
		coords = self.get_line_number_from_string(node.decl.coord)
		return {"name" : name, 
				"coordinates" : coords, 
				"documentation": ""}
	
	# not implemented yet
	def handle_structure(self, node, *args, **kwargs):
		return

	# not implemented yet
	def handle_typedef(self, node, *args, **kwargs):
		return

	# not implemented yet
	def handle_enum(self, node, *args, **kwargs):
		return

	def handle_define(self, node, *args, **kwargs):
		return

