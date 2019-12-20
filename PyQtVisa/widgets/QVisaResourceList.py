# ---------------------------------------------------------------------------------
# 	QVisaResourceList -> QWidget
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

# Import QT backends
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QStackedWidget, QComboBox, QLabel


import pyvisa
import re



class QVisaResourceList(QWidget):

	def __init__(self, _config):


		# Extends QWidget
		QWidget.__init__(self,)
		self._config = _config

		# Parse resrouces 
		self._parse_resources()

		# Generate main layout
		self._gen_main_layout()

	# Method to parse resources
	def _parse_resources(self):
		
		# Resources dictionary
		self.resources = {}

		# Get resource manger
		rm = pyvisa.ResourceManager()
		
		# Look through resource list
		for _resource in rm.list_resources():

			# Regex match for serial devices
			m = re.match(r'ASRL(\d+)::', _resource, re.ASCII)	
			if m:
				self.resources[ _resource ] = [ "RS-232", m[1] ]

			# Regex match for serial devices
			m = re.match(r'GPIB(\d+)::(\d+)', _resource, re.ASCII)	
			if m:
				self.resources[ _resource ] = [ "GPIB", m[1] , m[2] ]				


	# Get interfaces
	def _get_interfaces(self):

		_interfaces = []
		for _resource, _data in self.resources.items():
			if _data[0] not in _interfaces:
				_interfaces.append(_data[0])

		return _interfaces
				
	# Method to generate main layout
	def _gen_main_layout(self):

		self.layout = QHBoxLayout()

		self.interface_label = QLabel("<b>Interface</b>")
		self.interface_select = QComboBox()
		self.interface_select.addItems(self._get_interfaces())
		self.interface_select.currentTextChanged.connect(self.update_interface_pages)
		
		# For each interface, generate a page
		self.interface_pages = QStackedWidget()

		# Need a method to generate series of widgets for each interace type
		self.interface_pages.addWidget( self.gen_widgets("RS-232") )
		self.interface_pages.addWidget( self.gen_widgets("GPIB") )

		# Add widgets to layout
		self.layout.addWidget(self._config._gen_vbox_widget( [self.interface_label, self.interface_select] ) ,1)
		self.layout.addWidget(self.interface_pages,2)
		self.layout.setContentsMargins(0,0,0,0)

		# Set layout
		self.setLayout(self.layout)

	# Method to update interface pages
	def update_interface_pages(self):
	
		if self.interface_select.currentText() == "RS-232":
			self.interface_pages.setCurrentIndex(0)

	
		if self.interface_select.currentText() == "GPIB":
			self.interface_pages.setCurrentIndex(1)


	# Method to get resource string out of widgets
	def get_current_device(self):

		# Build the data array
		_selected = [self.interface_select.currentText()]

		# Add data from interface widgets 
		_interface_page = self.interface_pages.currentWidget()
		for _combobox in list( _interface_page.findChildren(QComboBox) ):
			_selected.append( _combobox.currentText() )

		# Find coresponding resource
		for _resource, _data in self.resources.items():
			if all(_ in _data  for _ in _selected):
				return _resource

	# Method to generate widgets for each communication mode
	def gen_widgets(self, _type):

		# Serial widgets
		if (_type == "RS-232"):

			# Create address combobox
			_addr_label = QLabel("<b>Address</b>")
			_addr = QComboBox()

			# Loop through all resources
			for _resource, _data in self.resources.items():

				# If data field is "RS-232"
				if _data[0] == "RS-232":

					# Add address to combobox
					_addr.addItem(_data[1])

			_widget = self._config._gen_vbox_widget( [_addr_label, _addr] )
			return _widget


		# GPIB Widgets
		if (_type == "GPIB"):

			# Create address combobox
			_board_label = QLabel("<b>Board</b>")
			_board = QComboBox()

			# Create address combobox
			_addr_label = QLabel("<b>Address</b>")
			_addr = QComboBox()


			# Loop through all resources
			for _resource, _data in self.resources.items():

				# If data field is "RS-232"
				if _data[0] == "GPIB":

					# Add board and address to combobox
					_board.addItem(_data[1])					
					_addr.addItem(_data[2])

			# create compund widgets
			_board_widget = self._config._gen_vbox_widget( [_board_label, _board] )
			_addr_widget = self._config._gen_vbox_widget( [_addr_label, _addr] )

			# Create final widget
			_widget = self._config._gen_hbox_widget( [_board_widget, _addr_widget] )
			return _widget