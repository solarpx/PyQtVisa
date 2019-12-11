# ---------------------------------------------------------------------------------
# 	QVisaApplication -> QWidget
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

#!/usr/bin/env python 
import time
import hashlib 

# Import QT backends
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QIcon

# Import QVisaWidgets
from .widgets.QVisaInstWidget import QVisaInstWidget
from .widgets.QVisaSaveWidget import QVisaSaveWidget

# Import QVisaDataObject
from .utils.QVisaDataObject import QVisaDataObject


#####################################
#  VISA APPLICATION CLASS
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
	def _get_data(self):
		return self._data

	# Method to reset data
	def _reset_data(self):
		self._data.reset()

	#####################################
	#  CONFIG WRAPPER METHODS
	#	

	# Method to get insturment handles
	def _get_inst_handles(self):
		return self._config._get_inst_handles()

	# Method to get insturment names
	def _get_inst_names(self):
		return self._config._get_inst_names()

	# Method to get insturment handles
	def _get_inst_byname(self, _name):
		return self._config._get_inst_byname(_name)	


	#####################################
	#  INST/SAVE WIDGET CONSTRUCTORS
	#	
	
	# Method to generate insturment widget
	def _gen_inst_widget(self):
		return QVisaInstWidget(self)

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
