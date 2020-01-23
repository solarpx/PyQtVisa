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
#	["<key0>"]
#		["<subkey0>"]	 = (list)
#		["<subkey1>"]	 = (list)
#		["<subkey2>"]	 = (list)
#
#	["<key1>"]
#		["<subkey>"]	 = (list)
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
		self.hash = self._gen_root_key()


	#####################################
	#  DICTIONARY METHODS
	#

	# Wrap dictionaty keys method
	def keys(self):
		return self.data.keys()

	# Wrap dictionaty items method
	def items(self):
		return self.data.items()

	# Method to get subkeys	
	def subkeys(self, _key):
		return self.data[_key].keys()	

	# Method to get subitems
	def subitems(self, _key):
		return self.data[_key].items()	

	# Method to get the root hash
	def roothash(self):
		return self.hash

	# Method to check is empty (numpy syntax)
	def empty(self):
		return True if self.data == {} else False

	# Method to reset data dictionaty
	def reset(self):
		self.data = {}

	#####################################
	#  DATA INTERACTION - KEY
	#

	# Generate hash
	def gen_hash(self, _salt=""):

		m = hashlib.sha256()		
		m.update( str( "%s%s"%( _salt, str(time.time())) ).encode() )
		return str( m.hexdigest()[:7] )

	# Initialize string as data key
	def add_key(self, _key=""):
		
		self.data[_key] = {}
		self.meta[_key] = {}
		return _key

	# Initialize hash for data key
	def add_hash_key(self, _salt=""):

		_hash = self.gen_hash(_salt)
		self.data[_hash] = {}
		self.meta[_hash] = {}
		return _hash 

	# Return data method 
	def get_key_data(self, _key):
		return self.data[_key]

	# Method to delete key
	def del_key(self, _key):
		
		if _key in self.data.keys():
			del self.data[_key]
			del self.meta[_key]

	# Method to check if all keys are empty		
	def keys_empty(self):
		
		for _key in self.data.keys():
			if self.data[_key] != {}:
				return False

		return True


	#####################################
	#  DATA INTERACTION - SUBKEY 
	#
	
	# Method to add a subkey	
	def add_subkey(self, _key, _subkey):
		if _subkey not in self.data[_key].keys():
			self.data[_key][_subkey] = []

	# Method to set subkeys
	def set_subkeys(self, _key, _subkeys):
		self.data[_key] = {_ : [] for _ in _subkeys} 

	# Method to get data field
	def get_subkey_data(self, _key, _subkey):
		return self.data[_key][_subkey]

	# Method to set data value (directly)
	def set_subkey_data(self, _key, _subkey, _data):
		self.data[_key][_subkey] = _data

	# Method to append data to field
	def append_subkey_data(self, _key, _subkey, _data):
		self.data[_key][_subkey].append(_data)

	# Method to delete subkey
	def del_subkey(self, _key, _subkey):
		if _subkey in self.data[_key].keys():
			del self.data[_key][_subkey]


	#####################################
	#  META INTERACTION
	#

	# Add generic metadata
	def _gen_root_key(self):
		_hash = self.gen_hash("_root")
		self.meta[ _hash ] = {}
		return _hash 

	# Add meta method
	def set_metadata(self, _key, _subkey, _data):

		# Shortcut to reference toplevel hash
		if _key == "__self__":
			_key = self.hash

		self.meta[_key][_subkey] = _data

	# Get meta method
	def get_metadata(self, _key, _subkey):

		# Shortcut to reference toplevel hash
		if _key == "__self__":
			_key = self.hash

		print(self.meta)

		# Return none if metadata has not been set	
		return self.meta[_key][_subkey] if _subkey in self.meta[_key].keys() else None


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
			if self.get_metadata(self.hash, "__note__") is not None:

				f.write( "*! note %s\n"%self.get_metadata(self.hash, "__note__") )
			
			# Write root hash
			f.write("*! hash %s\n\n"%self.hash)

			# Recall the form of self.data 
			# 	{ _key0 : {}, _key1 : {}, ...}
			for _key, _dict in self.data.items():

				# If measurement data exists on key
				if _dict is not None:

					# Write measrurement hash
					f.write( "#! __data__ %s\n"%( str(_key) ) )	

					# Write measurement metadata into header
					for _subkey, _data in self.meta[_key].items():
						f.write( "#! %s %s\n"%( str(_subkey), str(_data) ) ) 
					
					# Write data keys
					for _subkey in _dict.keys():

						f.write( "%s\t\t"%str(_subkey) )
					
					f.write("\n")
										
					# Write data values. 
					# Use length of first column for index iterator
					for i in range( len( _dict[ list(_dict.keys())[0] ] ) ):

						# Go across the dictionary keys on iterator
						for _subkey in _dict.keys():

							f.write( "%s\t"%str(_dict[_subkey][i]) )
					
						f.write("\n")

					f.write("\n\n")

			f.close()


	# Method to reconstruct data object from data file
	def read_from_file(self, filename, overwrite = False):
		
		# If data is not empty
		try:

			# We do not want to overwrite datastructures
			if self.data != {} and overwrite == False:
				raise PermissionError

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

						# Check for data header
						if _line[0] == "#!" and _line[1] == "__data__":

							# Cache key on __data__ 
							_key = _line[2]
							self.add_key(_key)

							# Loop through metadata lines
							while True:	

								# Next line contains the measurement keys
								_ = f.readline()
								_line = _.split()

								# If this is true, it is a metadata line
								if _line[0] == "#!":

									self.meta[_key][_line[1]] = _line[2]

								# Otherwise we have reached the keys	
								else:															

									# Initiaize empty list for each measurement key
									# via the class set_subkeys method
									_subkeys = _line
									self.set_subkeys(_key, _subkeys)

									# break the loop 
									break

							# Now loop throgh data lines
							while True:

								_ = f.readline()
								_line = _.split()

								# Next line should not be empty
								if _line != []:	

									# Read data into 
									for _subkey, _value in zip(_subkeys, _line):
									
										self.data[_key][_subkey].append( float(_value) )

								# If next line is empty we have reached the end of the data block
								else:

									# This will take top loop 
									break

		except PermissionError:
			print("Overwriting existing data is protected. Use read_from_file(_filename, overwrite=True) to overwrite")
