'''

			  [DESCRIPTION]
		 This file keeps help functions
	
				[CREATORS]
			 Name: Miasnenko Dmitry
	GitHub: https://github.com/YoungMeatBoy 

					REWRITE!
					REWRITE!
					REWRITE!
					REWRITE!
					REWRITE!
					REWRITE!
					REWRITE!
					REWRITE!
'''

from headgen.controller import Controller
import os

def info_get_functions_names(functions):
	res = ""
	for i, func in enumerate(functions):
		name = func["name"]
		res += f"    {i + 1} > {name}\n"
	return res




class StringWorker:
	def get_protection(self, path):
		filename = os.path.split(path)[1].replace('.', '_').upper()
		filename = f'__{filename}__'
		res = {'ifndef' : {'start' : f'#ifndef {filename}\n#define {filename}\n',
					 'end' : f'#endif /* {filename} */'},
		'pragma' : {'start' : '#pragma once\n',
					'end' : '\n'}
		}
		return res
	
	def get_info(self, filename, functions, structures, enums):
		filename = filename = os.path.split(filename)[1]
		functions_documentation = all([1 for _ in functions if _['documentation']])
		res = "/*\nThis file was generated automatically!\n"
		res += f"Header was created from file: \n    {filename}\n"
		res += f"Generated at         : {Controller(0, 0).current_time()}\n"
		res += f"Functions amount     : {len(functions)}   (Fully documentated: {functions_documentation})\n"
		res += f"Enums amount         : {len(enums)}\n"
		res += f"Structures amount    : {len(structures)}\n"
		res += "Functions' names:\n" + info_get_functions_names(functions)
		res += "*/\n\n"
		return res