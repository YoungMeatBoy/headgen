'''

			  [DESCRIPTION]
		 This file keeps FileWorker
		class which helps to with 
			files and thier paths
	
				[CREATORS]
			 Name: Miasnenko Dmitry
	GitHub: https://github.com/YoungMeatBoy 

'''

import os
import re
from typing import Callable, List


class FileWorker:
	
	def __init__(self, controller:Callable = None, filter_:Callable = None) -> None:
		# Tgis controller is a class which
		# organizates work with IO.
		self.controller = controller
		self.filter = filter_

	'''	
	@brief Checks if orrect directory given
	@param[in] directory str checking it
	'''
	def check_directory(self, directory:str) -> None:
		reason = {
				'message' : 'Given param is not a directory!',
				'reason'  : f'{directory}' + '\n' + ' '*15 + '^'
				 }
		if not os.path.isdir(directory):
			self.controller.finish(**reason)	
	
	'''	
	@brief finds files in a directory
	@param[in] directory directory to search in
	@param[in] filtering_filename name of ignore files
	@return list of found files
	'''
	def find_files(self, directory:str, filtering_filename:str=None) -> List[str]:
		self.check_directory(directory)
		self.controller.locked_print(f'\n[DIRECTORY OF SEARCHING] :\n     ➾  {directory}')
		self.controller.locked_print()
		self.controller.ask_to_continue()
		found_files:List[str] = list()
		for *root, files in os.walk(directory):
			for file in files:
				file_path = os.path.join(root[0], file)
				found_files.append(file_path)
		if self.filter:
			found_files = self.filter.filter_by_ignore_files(directory, filtering_filename, found_files)
		return found_files
	
	'''
	@brief gets name of the file
	@param[in] path str path of 
	@param[in] no_extension if you need no extension set to True
	@return str
	'''
	def get_file_name(self, path:str, no_extension:bool = False) -> str:
		splitted = path.split(os.sep)
		res = splitted.pop()
		if no_extension:
			res = self.remove_extension_from_filename(res)
		return res
	
	'''
	@brief Removes extension from a filename
	@param[in] path str path to file
	@return result
	'''
	def remove_extension_from_filename(self, path:str) -> str:
		pattern = r'\w{1,}[.]\w{1,}'
		pattern = re.compile(pattern)
		found = re.match(pattern, path)
		if found:
			return found[0].split('.')[0] 
		else:
			reason = {'message' : 'Incorrect filename given!',
					  'reason'  : 'f{path} is bad'}
			self.controller.finish(**reason)

	'''
	@brief Checks if file exists
	@param[in] filename path to a file
	@return bool
	'''
	def accept_file(self, filename:str) -> bool:
		res = os.path.isfile(filename)
		if not res:
			reason = {
				'message'  : 'Incoorect file path given!',
				'reason'   : f'    {filename}' + '\n    ^'
			}
			self.controller.finish(**reason)
		return True
