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
	@brief Makes function signature
	@param[in] line dirty line with signatre
	@return str signature
	'''
	def get_function_signature(self, line:str) -> str:	
		return line.split('{')[0].strip() + ';\n'

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
