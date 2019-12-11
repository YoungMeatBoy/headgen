'''

			  [DESCRIPTION]
		 This file keeps FilesFilter
	class which helps to filter founf files
	
				[CREATORS]
			 Name: Miasnenko Dmitry
	GitHub: https://github.com/YoungMeatBoy 

'''

import os
import re
from fnmatch import fnmatch
from typing import Callable, List

from headgen.file_worker import FileWorker


class FileFilter:
	def __init__(self, controller:Callable = None) -> None:
		self.cache_files = []
		self.controller = controller
		self.fileworker  = FileWorker(controller)
	
	'''
	@brief Takes all regexp patterns in the file and compiles them 
	@param[in] file name of the file
	@return List of compiled regexp patterns
	'''
	def take_regexp_patterns_from_file(self, file:str) -> List:
		if not os.path.isfile(file):
			reason = {
				'message': 'Could not read filtering file!',
				'reason' : f'{file} is not a file path!'
			}
			self.controller.finish(**reason)
		else:
			result:List = list()
			with open(file, 'r', encoding = 'utf-8') as opened_file:	
				for line_ind, line in enumerate(opened_file):
					try:
						result.append(line.strip())
					except Exception:
						reason = {
							'message' : 'Impossible to read all patterns from the file!',
							'reason'  : f'Failed to compile line > {line} < on line {line_ind} in file {file}'
						}
						self.controller.finish(**reason)
			return result

	'''
	@brief Deletes files matching patterns
	@param[in] files list of files to be filtered
	@param[in] patterns list of the patterns
	@return list of files
	'''
	def delete_files_matching_patterns(self, files:List[str], patterns:List) -> List:
		for pattern in patterns:
			for file in files:
				if fnmatch(file, pattern):
					files.remove(file)
		return files

	'''	
	@brief
	@param[in] diretory str directory of starting searching
	@param[in] filtering_filename str name of the ignore file
	@return found paths of ignore files
	'''
	def find_filtering_files_recursively(self, directory:str, filtering_filename:str) -> List:
		if self.cache_files:	
			files = self.cache_files
		else:
			files = self.find_files(directory)
		result:List[str] = list()
		for file in files:
			if filtering_filename in file:
				result.append(file)
		return result

	'''	
	@brief get all patterns from all ignore files
	@param[in] directory str directory to search in
	@param[in] filtering_filename name of ignoe file
	'''
	def get_all_patterns_recursively(self, directory:str, filtering_filename:str) -> List:
		res:List = list()
		files = self.find_filtering_files_recursively(directory, filtering_filename)
		for file in files:
			res += self.take_regexp_patterns_from_file(file)
		return res

	'''
	@brief filter by found ignore files
	@param[in] directory the directory to search
	@param[in] filtering_filename name of the ignore file
	@param[in] files list of files
	@return filtered files
	'''
	def filter_by_ignore_files(self, directory:str, filtering_filename:str, files:List[str]) -> List[str]:
		from pprint import pprint
		patterns = self.get_all_patterns_recursively(directory, filtering_filename)
		files = self.delete_files_matching_patterns(files, patterns)
		return files

	'''
	@brief copy of fileworker.found_files
	@param[in] directory the directory to search in
	@return files
	'''
	def find_files(self, directory:str) -> List[str]:
		self.fileworker.check_directory(directory)
		found_files:List[str] = list()
		for *root, files in os.walk(directory):
			for file in files:
				file_path = os.path.join(root[0], file)
				found_files.append(file_path)
		return found_files
	
	'''
	@brief finds all files which matches the pattern
	@param[in] files list of files
	@param[in] patta
	@return List of found files
	'''
	def find_all(self, files:List[str], pattern:str) -> List[str]:
		res = list()
		for file in files:
			if fnmatch(file, pattern):
				res.append(file)
		return res

	'''
	@brief Removes empty files from a list
	@param[in] files list of files
	@return filtered list of files
	'''
	def remove_empty_files(self, files:List[str]) -> List[str]:
		#import os
		for file in files:
			if os.path.getsize(file) <= 0:
				files.remove(file)
		return files