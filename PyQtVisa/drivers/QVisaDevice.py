# ---------------------------------------------------------------------------------
# 	QVisaDevice
# 	Copyright (C) 2019 Michael Winters
#	mwchalmers@protonmail.com
# ---------------------------------------------------------------------------------
# 
# 	Permission is hereby granted, free of charge, to any person obtaining a copy
# 	of this software and associated documentation files (the "Software"), to deal
# 	in the Software without restriction, including without limitation the rights
# 	to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# 	copies of the Software, and to permit persons to whom the Software is
# 	furnished to do so, subject to the following conditions:
# 	
# 	The above copyright notice and this permission notice shall be included in all
# 	copies or substantial portions of the Software.
# 	
# 	THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# 	IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# 	FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# 	AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# 	LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# 	OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# 	SOFTWARE.
#

#!/usr/bin/env python 
# -*- coding: utf-8 -*-
import pyvisa

# Basic driver file for insturment
class QVisaDevice:

	# Initialize
	def __init__(self, _comm, _addr, _name="QVisaDevice"):

		# Cache initialization data
		self.comm = _comm
		self.addr = _addr 
		self.name = _name

		# Helper strings
		self.type = _name

		# Extract insturment handle for Keithley
		self.rm = pyvisa.ResourceManager()

		# Initialize communication modes
		if _comm in ["gpib", "GPIB"]:
			self.port = "ASRL::%s"%self.addr

			self.gpib()

		if _comm in ["rs232", "RS232", "RS-232"]:	
			self.rs232()

		# Create buffer object
		self.buffer = ""

	# GPIB Device
	# Attempt to open resource. 
	def gpib(self):	

		self.inst = self.rm.open_resource('GPIB0::%s::INSTR'%self.addr)
		self.inst.timeout = 2000
		self.inst.clear()

		# Define port
		self.port = "GPIB0::%s"%(self.addr)

		# Append Address to name
		self.name = "%s GPIB0::%s"%(self.name, self.addr)

	# Serial Device
	# Attempt to open resource. 
	def rs232(self):
		
		self.inst = self.rm.open_resource('ASRL%s::INSTR'%self.addr)
		self.inst.timeout = 2000
		self.inst.clear()		

		# Define port
		self.port = "ASRL::%s"%(self.addr)

		# Append Address to name
		self.name = "%s %s"%(self.name, self.port)


	# Close instrument on program termination
	def close(self): 
		self.inst.close()

	# Write command
	def write(self, _data):
		self.inst.write(_data)
	
	# Query command. Only use when reading data	
	def query(self, _data, print_buffer=False):

		# Try to communicate with device
		self.buffer = self.inst.query(_data)

		# Option to print buffer
		if print_buffer:
			print(self.buffer)

		# Return buffer	
		return self.buffer