'''

			  [DESCRIPTION]
		 This file keeps Maker
		class which helps generate 
				headers
	
				[CREATORS]
			 Name: Miasnenko Dmitry
	GitHub: https://github.com/YoungMeatBoy 

'''

from headgen.visitor import MainVisitor
from headgen.string_worker import StringWorker


class Maker:
	def __init__(self,  flags, fileworker, controller):
		self.flags = flags or {'protection_type' : 'ifndef'}
		self.fileworker = fileworker
		self.main_visitor = MainVisitor(controller)
		self.controller = controller
		self.string_worker = StringWorker()
	
	'''
	@brief Creates header for *.c files
	@param[in] file path to *.c file
	@return error code	
	'''
	def create_header(self, file):
		# using hack for replacing extension
		# reverse -> replace -> replace
		header_path = file[::-1].replace('c.', 'h.', 1)[::-1]
		
		# visiting ast
		ast = self.main_visitor.get_ast(file)
		self.main_visitor.visit(ast)

		# taking all functions
		functions = self.main_visitor.get_functions(file)
		
		# finding documentation for functions and links them
		self.main_visitor.get_documentation(file, functions)
		
		#taking protection
		protection = self.string_worker.get_protection(header_path)
		
		# taking info
		info = self.string_worker.get_info(file, functions = functions)
  
		includes, sort_includes = self.main_visitor.get_includes(file)
		includes = self.main_visitor.prettify_includes(includes, sort_includes)

		defines_before, defines_after = self.main_visitor.get_defines(file)


		structures = self.main_visitor.get_structures(file)
		enums = self.main_visitor.get_enums(file)
  

		with open(header_path, 'w') as header:
			# writing info
			header.write(info)

			# writing protection
			header.write(protection[self.flags['protection_type']]['start'])
			
			header.write('\n')
			for define in defines_before:
				header.write(define + '\n')

			#writing includes
			header.write('\n')
			for inc in includes:
				header.write(inc + '\n')
			header.write('\n')

			for define in defines_after:
				header.write(define + '\n')

			header.write('\n')
			# writing enums
			for en in enums:
				header.write(en + '\n')

			header.write('\n')
			#writing structures
			for struct in structures:
				header.write(struct + '\n')

			# writing functions
			for function in functions:
				header.write('\n')
				header.write(function['documentation'])
				header.write(function['signature'])
				header.write('\n')

			header.write(protection[self.flags['protection_type']]['end'])


