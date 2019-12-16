
import os
from argparse import ArgumentParser
from pprint import pprint

from headgen.file_worker import FileWorker
from headgen.controller import Controller
from headgen.file_filter import FileFilter 
from headgen.maker import Maker
from colors import *
from colorama import init
import tableprint
init()


parser = ArgumentParser()
	
parser.add_argument("-p"  , "--pragma"           , help = "Set pragma protection.",                                 action = "store_true", required = False)
parser.add_argument("-if" , "--ifndef"           , help = "Set ifndef protection.",                                 action = "store_true", required = False, default = True)
parser.add_argument("-a"  , "--ask"              , help = "Wу will ask you before doing anything",                  action = "store_true", required = False)
parser.add_argument("-f"  , "--file"             , help = "Path to the file for which you want to create a header.",                       required = False, default = "")
parser.add_argument("-d"  , "--dir"              , help = "Directory of file searching.",                                                  required = False, default = "")
parser.add_argument("-dp" , "--disable_printing" , help = "Should we print info?",                                  action = "store_true", required = False, default = False)

args = parser.parse_args()

IGNORE_FILENAME = '.headignore'

controller = Controller(print_flag = not args.disable_printing,
						ask_flag = args.ask,)
filefilter = FileFilter(controller)
fileworker = FileWorker(controller, filefilter)
maker_flags = {
	'protection_type' : 'pragma' if args.pragma else 'ifndef'
}
maker = Maker(maker_flags, fileworker, controller)

if args.file:
	# Checking if file
	# path is correct
	if fileworker.accept_file(args.file):
		controller.locked_print(cyan('processing'), magenta(f'     {args.file}'))

		controller.ask_to_continue()

		maker.create_header(args.file)

		controller.success()
else:
	parent_directory = args.dir or os.getcwd()
	controller.locked_print(cyan('\nsearching in'), magenta(f'\n     {parent_directory.lower()}'))
	controller.locked_print()
	controller.ask_to_continue()
	files = fileworker.find_files(parent_directory, IGNORE_FILENAME)
	files = fileworker.filter.remove_empty_files(files)
	files = fileworker.filter.find_all(files, '*.c')
	
	if not files:
		controller.finish('Impossible to find *.c files!',
							'No files in this directory!')
	else:
		controller.locked_print(cyan('found source files'))
		for file in files:
			no_parent_dir = file.replace(parent_directory, '')
			controller.locked_print(magenta(f'     {no_parent_dir.lstrip(os.sep)}'))
		controller.locked_print()
		
		controller.ask_to_continue()

		controller.locked_print(cyan('processing'))
		for file in files:
			controller.locked_print(magenta(f'     {file.lower()}'))
			maker.create_header(file)
		controller.locked_print()
	
 


