# ---------------------------------------------------------------------------------
# 	QVisaDevice 
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
import pyvisa
import re

# Basic driver file for insturment
class QVisaDevice:

	# Initialize
	def __init__(self, _resource, _type="QVisaDevice"):

		# Call parse resource
		self.parse_resource(_resource, _type)

		# Build alias table
		self.alias_table()

	def parse_resource(self, _resource, _type):

		# Create data object
		self.__resource = {}

		# Extract insturment handle for Keithley
		rm = pyvisa.ResourceManager()

		# Check if resource is in driver table
		if _resource in rm.list_resources():
		
			self.__resource["inst"] = rm.open_resource(_resource)

			# Standard serial port 
			m = re.match(r'ASRL(\d+)::\w+$',  _resource, re.ASCII)
			if m:			

				# Resource sting
				self.__resource["resource"] = m[0]

				# Resource data
				self.__resource["comm"] = "ASRL"
				self.__resource["addr"] = m[1]
				self.__resource["type"] = _type
				self.__resource["name"] = "%s ASRL%s"%(_type, str(m[1]))

			# GPIB device on board
			m = re.match(r'GPIB(\d+)::(\d+)::\w+$',  _resource, re.ASCII)
			if m:

				# Resource sting
				self.__resource["resource"] = m[0]

				# Resource data
				self.__resource["comm"] = m[1]
				self.__resource["addr"] = m[2]
				self.__resource["type"] = _type
				self.__resource["name"] = "%s GPIB%s::%s"%(_type, str(m[1]), str(m[2]))
	
	
	# Return resource dictionary
	def get_resource(self):
		return self.__resource

	# Return resource property
	def get_property(self, _key):
		return self.__resource[_key] if _key in self.__resource.keys() else None


	####################################
	#	HARDWARE IO
	#

	# Close instrument on program termination
	def close(self): 
		self.__resource["inst"].close()
		self.__resource = {}

	# Write command
	def write(self, _data):
		self.__resource["inst"].write(_data)
	
	# Query command. Only use when reading data	
	def query(self, _data, print_buffer=False):

		_buffer = self.__resource["inst"].query(_data)

		# Option to print buffer
		if print_buffer:
			print(_buffer)

		return _buffer

	####################################
	#	GENERAL
	#	

	# Identify command
	def IDN(self):
		return self.query('*IDN?')

	# Reset command. Abort all activities and initialize the device
	def RST(self):
		self.write('*RST')

	# Self test query. Perform a self-test. Returns ‘0'  if self test 
	# completed without errors, all other values determine an error cause.
	def TST(self):
		self.write("*TST?")

	####################################
	#	SYNCHRONZATION
	#	

	# OPeration Complete command. Set the Operation Complete bit in the
	# Event Status Register to '1' when all pending commands and/or queries 
	# are finished. The controller can read this bit with the *ESR? query.
	def OPC(self):
		self.write('*OPC')

	# OPeration Complete query. This query returns '1' when all pending
	# commands and/or queries are finished.
	def OPC_query(self):
		return self.query('*OPC?')

	# Wait command. Wait until all pending commands and queries are processed.
	def WAI(self):
		self.write('*WAI')

	# Trigger command. Execute trigger function(s).
	def TRG(self):
		self.write('*TRG')

	####################################
	#	INSTURMENT STATUS
	#	

	# Clear Status command. Clears the whole status structure	
	def CLS(self):
		self.write('*CLS')

	# Event Status Enable register (ESE) is used to control which bits from the ESR 
	# are summarized in the ESB bit (5) in the Status Byte register (STB). This ESE 
	# register is read/write.
	def ESE(self):
		self.write('*ESE')

	# Standard Event Status Enable query	
	def ESE_query(self):
		return self.query('*ESE?')

	# Event Status Register: contains the actual status information 
	# derived from the instrument. This register is read only
	def ESR_query(self):
		return self.query('*ESR?')

	# Service Request Enable command. Modify the contents of the Service Request
	# Enable Register.	
	def SRE(self):
		self.write('*SRE')

	# Service Request Enable query. Return the contents of the Service Request 
	# Enable Register	
	def SRE_query(self):
		return self.query('*SRE')

	# Status Byte query. Return the contents of the Status Byte Register.
	def STB_query(self):
		return self.query('*STB?')


	####################################
	#	ALIAS TABLE
	#			
	def alias_table(self):

		# General shortcuts
		self.idn = self.IDN
		self.rst = self.RST
		self.tst = self.TST
		
		# Synchronization 
		self.wai = self.WAI 
		self.opc = self.OPC 
		self.opc_query = self.OPC_query
		self.trg = self.TRG

		# Insturment Status
		self.ese = self.ESE
		self.ese_query = self.ESE_query
		self.esr_query = self.ESR_query
		self.sre = self.SRE
		self.sre_query = self.SRE_query
		self.stb_query = self.STB_query
