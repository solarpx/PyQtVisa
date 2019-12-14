# ---------------------------------------------------------------------------------
# 	QVisaDataObject
#	Copyright (C) 2019 Michael Winters
#	github: https://github.com/mesoic
#	email:  mesoic@protonmail.com
# ---------------------------------------------------------------------------------
#	
#	Permission is hereby granted, free of charge, to any person obtaining a copy
#	of this software and associated documentation files (the "Software"), to deal
#	in the Software without restriction, including without limitation the rights
#	to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#	copies of the Software, and to permit persons to whom the Software is
#	furnished to do so, subject to the following conditions:
#	
#	The above copyright notice and this permission notice shall be included in all
#	copies or substantial portions of the Software.
#	
#	THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#	IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#	FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#	AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#	LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#	OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#	SOFTWARE.
#

#!/usr/bin/env python 
# -*- coding: utf-8 -*-
import time
import hashlib 

# Class to manage measurement data collected by PyQtVisa applications. Data always 
# takes the following format: 
#
#	["<hash0>"]
#		["__type__"] = (string)
#		["<var0>"]	 = (list)
#		["<var1>"]	 = (list)
#		["<var2>"]	 = (list)
#
#	["<hash1>"]
#		["__type__"] = (string)
#		["<var1>"]	 = (list)
#
# The class contains methods to generate such data structures in software, to write
# data objects into files and to read back data from files losslessly.
#

class QVisaDataObject:

	def __init__(self):

		# Initialize data and meta dictionaries
		self.data = {}
		self.meta = {}

		# Generate hash for data object
		self.hash = self.gen_root_key("_root")


	#####################################
	#  DICTIONARY METHODS
	#

	# Wrap dictionaty keys method
	def keys(self):
		return self.data.keys()

	# Wrap dictionaty items method
	def items(self):
		return self.data.items()

	# Method to return data	
	def data(self):	
		return self.meta

	# Method to return meta
	def meta(self):	
		return self.meta

	# Method to get the root hash
	def hash(self):
		return self.hash

	# Method to check is empty (numpy syntax)
	def empty(self):
		return True if self.data == {} else False

	# Method to reset data dictionaty
	def reset(self):
		self.data = {}
	

	#####################################
	#  DATA INTERACTION
	#

	# Generate hash
	def gen_hash(self, _salt=""):

		m = hashlib.sha256()		
		m.update( str( "%s%s"%( _salt, str(time.time())) ).encode() )
		return str( m.hexdigest()[:7] )

	# Generate hash for data key
	def gen_data_key(self, _salt=""):
		
		_hash = self.gen_hash(_salt)
		self.data[ _hash ] = {}
		self.meta[ _hash ] = {}
		return _hash 
	
	# Method to add data fields
	def add_data_fields(self, _hash, _fields):
		self.data[_hash] = {_ : [] for _ in _fields} 

	# Method to get data field
	def get_data_field(self, _hash, _key):
		return self.data[_hash][_key] if _key in self.data[_hash].keys() else None

	# Method to set data field
	def set_data_value(self, _hash, _key, _value):
		self.data[_hash][_key] = _value
	
	# Method to append data field
	def append_data_value(self, _hash, _key, _value):
		self.data[_hash][_key].append(_value)

	# Return data method
	def get_data(self, _hash):
		return self.data[_hash] if _hash in self.data.keys() else None

	#####################################
	#  META INTERACTION
	#

	# Add generic metadata
	def gen_root_key(self, _salt=""):
		_hash = self.gen_hash(_salt)
		self.meta[ _hash ] = {}
		return _hash 

	# Add meta method
	def set_meta(self, _hash, _key, _value):

		# Shortcut to reference toplevel hash
		if _hash == "__self__":
			_hash = self.hash

		self.meta[_hash][_key] = _value

	# Get meta method
	def get_meta(self, _hash, _key):

		# Shortcut to reference toplevel hash
		if _hash == "__self__":
			_hash = self.hash

		return self.meta[_hash][_key] if _key in self.meta[_hash].keys() else None

	#####################################
	#  FILE IO
	#	
	
	def write_to_file(self, _filename):

		# Open file pointer	
		f = open(_filename, 'w+')

		# Start write sequence
		with f:	
		
			# Write data header
			f.write("*! QVisaDataObject v1.1\n")
			
			# If a note exists write it
			if self.get_meta(self.hash, "__note__") is not None:

				f.write( "*! note %s\n"%self.get_meta(self.hash, "__note__") )
			
			# Write root hash
			f.write("*! hash %s\n"%self.hash)

			# Only save if data exists on a given key
			for _hash, _data in self.items():

				# If measurement data exists on key
				if _data is not None:

					# Write measurement key header
					if self.get_meta(_hash, "__type__") is not None:

						f.write( "#! %s %s\n"%( self.get_meta(_hash, "__type__"), str(_hash) ) ) 

					else:
						
						f.write( "#! %s\n"%str(_hash) ) 
					
					# Write data keys
					for _field in _data.keys():

						f.write( "%s\t\t"%str(_field) )
					
					f.write("\n")
										
					# Write data values. 
					# Use length of first column for index iterator
					for i in range( len( _data[ list(_data.keys())[0] ] ) ):

						# Go across the dictionary keys on iterator
						for _field in _data.keys():

							f.write( "%s\t"%str(_data[_field][i]) )
					
						f.write("\n")

					f.write("\n\n")

			f.close()


	# Method to reconstruct data object from data file
	def read_from_file(self, filename, overwrite = False):
		
		# If data is not empty
		try:

			# We do not want to overwrite datastructures
			if self.data != {} and overwrite == False:
				raise AttributeError

			# Unless explicitly specified 
			else: 
				self.data = {}

			
			# Open file pointer	
			f, _ = open(filename, 'r'), True

			# Start the read sequence
			with f:

				while _:

					_ = f.readline()
					_line = _.split()

					# If line is not empty
					if _line != []:	

						# Check for file header 
						if _line[0] == "*!":

							# If a note is included
							if _line[1] == "note":

								# Extract note
								self.add_note( " ".join(_line[2:]) )


						# Check for data header
						if _line[0] == "#!":

							_type = _line[1] # Measurement type
							_hash = _line[2] # Measurement hash				
							self.add_type( _line[1] )

							# Next line contains the measurement keys
							_ = f.readline()
							_keys = _.split()

							# Initiaize empty list for each measurement key
							self.data[ _hash ] = { _: [] for _ in _keys }

							# Now loop throgh data lines
							while True:

								_ = f.readline()
								_line = _.split()

								# Next line should not be empty
								if _line != []:	

									# Read data into 
									for _k, _d in zip(_keys, _line):
									
										self.data[ _hash ][_k].append( float(_d) )

								# If next line is empty we have reached the end of the data block
								else:

									# This will take top loop 
									break

		except AttributeError:
			print("Overwriting existing data is protected. Use read_from_file(_filename, overwrite=True) to overwrite")
