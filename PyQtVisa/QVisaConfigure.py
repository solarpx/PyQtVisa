# ---------------------------------------------------------------------------------
# 	QVisaConfigure -> QWidget
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

#####################################
#  QVISA CONFIGURE CLASS
#	

#!/usr/bin/env python 
# -*- coding: utf-8 -*-
import visa
import time
import threading 
import numpy as np

# Import QT backends
import os
import sys
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QMessageBox 

# Import QVisaInstWidget and QVisaCommWidget
from .widgets.QVisaDeviceSelect import QVisaDeviceSelect
from .widgets.QVisaDeviceControl import QVisaDeviceControl

# The purpouse of this object is to bind a list pyVisaDevices to a QWidget 
# in a configuration context. The idea is to first construct a QVisaConifg
# object which contains the list of insturment handles, and then pass the 
# object to QVisaWidget objects which can interact with the insturments
#

class QVisaConfigure(QWidget):

	# Initialization
	def __init__(self):

		QWidget.__init__(self)
		self.Devices = []

	# Add QVisaDevice objects
	def add_device(self, _device):
		self.Devices.append(_device)

	# Get all insturment handles
	def get_devices(self):
	
		if self.Devices != []:
			return self.Devices
		else:
			return None 
			
	# Get all device names
	def get_device_names(self):

		if self.Devices != []:
			return [_.get_property("name") for _ in self.Devices]	
		else:	
			return None

	# Get device by resrouce string 
	def get_device(self, _resource):

		# Loop through insturment list
		for _ in self.Devices:
			if _.get_property("resource") == _resource:
				return _

		# If we do not find device return None		
		return None

	# Get device by name
	def get_device_by_name(self, _name):

		# Loop through insturment list
		for _ in self.Devices:
			if _.get_property("name") == _name:
				return _

		# If we do not find device return None		
		return None

	# Close devices on app.exit()
	def close_devices(self):

		for Device in self.Devices:

			Device.close()

	# Helper method to pack widgets into hbox
	def _gen_hbox_widget(self, _widget_list):
	
		_widget = QWidget()
		_layout = QHBoxLayout()
		for _w in _widget_list:
			_layout.addWidget(_w)

		_layout.setContentsMargins(0,0,0,0)
		_widget.setLayout(_layout)
		return _widget	

	# Helper method to pack widgets into vbox
	def _gen_vbox_widget(self, _widget_list):
	
		_widget = QWidget()
		_layout = QVBoxLayout()
		for _w in _widget_list:
			_layout.addWidget(_w)

		_layout.setContentsMargins(0,0,0,0)
		_widget.setLayout(_layout)
		return _widget

	# Method to generate device select widget
	def _gen_device_select(self):
		return QVisaDeviceSelect(self)

	# Method to generate communication widget
	def _gen_device_control(self):
		return QVisaDeviceControl(self)

