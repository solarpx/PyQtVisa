# ---------------------------------------------------------------------------------
# 	QVisaApplication -> QWidget
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

# Import QT backends
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QIcon

# Import QVisaWidgets
from .widgets.QVisaDeviceSelect import QVisaDeviceSelect
from .widgets.QVisaSaveWidget import QVisaSaveWidget

# Import QVisaDataObject
from .utils.QVisaDataObject import QVisaDataObject


#####################################
#  QVISA APPLICATION CLASS
#	

# The purpouse of the QVisaApplication object is to bind a list pyVisaDevices to a QWidget 
# It provides a basic framework for constructing user interfaces for interacting with GPIB 
# hardware. 

class QVisaApplication(QWidget):

	# Initialization: Note that _config is a QVisaConfig object 
	# which contains a list of pyVisaDevices	
	def __init__(self, _config):

		QWidget.__init__(self)

		# Data and configuration
		self._data = QVisaDataObject()
		self._config = _config 

	# Getter method for data object
	def _get_data_object(self):
		return self._data

	# Method to reset data
	def _reset_data_object(self):
		self._data.reset()

	#####################################
	#  CONFIG WRAPPER METHODS
	#	

	def get_devices(self):
	
		if self._config.Devices != []:
			return self._config.Devices
		else:
			return None 
				
	# Get all device names
	def get_device_names(self):

		if self._config.Devices != []:
			return [_.get_property("name") for _ in self._config.Devices]	
		else:	
			return None

	# Get device by name
	def get_device_by_name(self, _name):

		# Loop through insturment list
		for _ in self._config.Devices:
			if _.get_property("name") == _name:
				return _

		# If we do not find device return None		
		return None


	#####################################
	#  CONFIG WRAPPER METHODS
	#	

	# Method to set app-level meta
	def _set_app_metadata(self, key, value):
		self._data.set_metadata( "__self__" , key, value)

	# Method to get app-level meta
	def _get_app_metadata(self, key):	
		return self._data.get_metadata("__self__", key)

	#####################################
	#  INST/SAVE WIDGET CONSTRUCTORS
	#	
	
	# Method to generate insturment widget
	def _gen_device_select(self):
		return QVisaDeviceSelect(self)

	# Method to generate the standard save widget
	def _gen_save_widget(self):
		return QVisaSaveWidget(self)


	#####################################
	#  LAYOUT SHORTCUTS
	#					

	# Helper methods to handle icons
	def _set_icon(self, _icon):
		
		self._icon = _icon

	def _get_icon(self):
		
		try:
			return self._icon
		except AttributeError:
			return QIcon()

	# Helper method to pack widgets into hbox
	def _gen_hbox_widget(self, _widget_list):
	
		_widget = QWidget()
		_layout = QHBoxLayout()
		for _w in _widget_list:
			_layout.addWidget(_w)

		_layout.addStretch(1)
		_layout.setContentsMargins(0,0,0,0)
		_widget.setLayout(_layout)
		return _widget	

	# Helper method to pack widgets into vbox
	def _gen_vbox_widget(self, _widget_list):
	
		_widget = QWidget()
		_layout = QVBoxLayout()
		for _w in _widget_list:
			_layout.addWidget(_w)

		_layout.addStretch(1)
		_layout.setContentsMargins(0,0,0,0)
		_widget.setLayout(_layout)
		return _widget
