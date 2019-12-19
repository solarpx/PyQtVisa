# ---------------------------------------------------------------------------------
# 	QVisaInitWidget -> QWidget
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

# Import QT backends
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QComboBox, QLabel, QStackedWidget, QSpinBox, QPushButton, QMessageBox
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon


# Impot QVisaInstWidget widget
from .QVisaInstWidget import QVisaInstWidget

class QVisaCommWidget(QWidget):

	def __init__(self, _config):

		# Call QWidget init
		QWidget.__init__(self)

		# Cache calling QVisaConfigure object
		self._config = _config

		# Generate main layout
		self.gen_main_layout()

		# Callbacks 
		self._init_callback = None
		self._inst_callback = None

	def gen_main_layout(self):
	
		# Create configuration layout
		self.layout = QVBoxLayout()

		# Initialize device button
		self.init_button = QPushButton("Initialize Device")
		self.init_button.clicked.connect(self._run_init_callback)
		self.inst_widget = QVisaInstWidget(self._config)

		# Configuration selector
		self.layout.addWidget(self.init_button)
		self.layout.addWidget(self.gen_conf_widget())
		self.layout.addWidget(QLabel("<b>Select Instrument</b>"))
		self.layout.addWidget(self.inst_widget)

		self.setLayout(self.layout)

	# Mode select widget
	def gen_conf_widget(self):
		
		# Generate widget
		self.comm_widget = self.gen_comm_widget()		

		# Address spinbox and button as pags
		self.comm_pages = QStackedWidget()
		self.comm_pages.addWidget(self.gen_gpib_widget())
		self.comm_pages.addWidget(self.gen_rs232_widget())
		self.comm_pages.setCurrentIndex(0)

		# Pack widgets into QHBoxLayout
		self.conf_layout = QHBoxLayout()
		self.conf_layout.addWidget(self.comm_widget)
		self.conf_layout.addWidget(self.comm_pages)
		self.conf_layout.setContentsMargins(0,0,0,0)

		# Create widget, set layout, and return
		self.conf_widget = QWidget()
		self.conf_widget.setLayout(self.conf_layout)
		return self.conf_widget

	# Communication mode selection (GPIB/RS232)
	def gen_comm_widget(self):

		# Communication com select
		self.comm_select_label = QLabel("<b>Connection</b>")
		self.comm_select = QComboBox()
		self.comm_select.addItems(["GPIB", "RS-232"])	
		self.comm_select.currentTextChanged.connect(self.update_comm_pages)

		# Add widgets to layout 
		self.comm_layout = QVBoxLayout()
		self.comm_layout.addWidget(self.comm_select_label)
		self.comm_layout.addWidget(self.comm_select)
		self.comm_layout.setContentsMargins(0,0,0,0)

		# Set layout and return widget
		self.comm_widget = QWidget()
		self.comm_widget.setLayout(self.comm_layout)
		
		return self.comm_widget	

	# GPIB congifuration widget
	def gen_gpib_widget(self):

		# GPIB Address selector
		self.gpib_label = QLabel("<b>GPIB Address</b>")
		self.gpib_value = QSpinBox()
		self.gpib_value.setMinimum(0)
		self.gpib_value.setMaximum(30)
		self.gpib_value.setValue(24)

		# Add widgets to layout
		self.gpib_layout = QVBoxLayout()
		self.gpib_layout.addWidget(self.gpib_label)
		self.gpib_layout.addWidget(self.gpib_value)
		self.gpib_layout.setContentsMargins(0,0,0,0)

		# Set widget layout and return widget
		self.gpib_widget = QWidget()
		self.gpib_widget.setLayout(self.gpib_layout)

		return self.gpib_widget

	# RS232 congifuration widget
	def gen_rs232_widget(self):

		# GPIB Address selector
		self.rs232_label = QLabel("<b>RS-232 Port</b>")
		self.rs232_value = QSpinBox()
		self.rs232_value.setMinimum(0)
		self.rs232_value.setMaximum(10)
		self.rs232_value.setValue(5)

		# Add widgets to layout
		self.rs232_layout = QVBoxLayout()
		self.rs232_layout.addWidget(self.rs232_label)
		self.rs232_layout.addWidget(self.rs232_value)
		self.rs232_layout.setContentsMargins(0,0,0,0)

		# Set widget layout
		self.rs232_widget = QWidget()
		self.rs232_widget.setLayout(self.rs232_layout)
	
		return self.rs232_widget

	# Method to get current insturemnt
	def get_current_inst(self):

		_name = self.inst_widget.currentText() 
		_inst = self._config._get_inst_byname(_name)

		if _inst is not None:
			return _inst

		else: 
			return None

	# Update comm_pages (QSpinBox, QLabel)
	def update_comm_pages(self):

		# GPIB Mode
		if self.comm_select.currentText() == "GPIB":
			self.comm_pages.setCurrentIndex(0)

		# RS232 Mode
		if self.comm_select.currentText() == "RS-232":
			self.comm_pages.setCurrentIndex(1)

	# Methods to get mode and callback
	def get_addr(self):
		
		if self.comm_select.currentText() == "GPIB":
			return self.gpib_value.value()

		if self.comm_select.currentText() == "RS-232":
			return self.rs232_value.value()

	# Methods to get mode and callback
	def get_comm(self):
		return self.comm_select.currentText()

	def get_icon(self):

		try :
			return self._config._icon
		except: 
			return QIcon()

	# Return port string
	def get_port(self):

		if self.get_comm() == "GPIB":
			return "GPIB0::%s"%self.get_addr()

		if self.get_comm() == "RS-232":
			return "ASRL::%s"%self.get_addr()


	# Refresh instrument widget
	def refresh(self):
		self.inst_widget.blockSignals(True)
		self.inst_widget.refresh( self._config )
		self.inst_widget.blockSignals(False)


	# initalize Insturment
	def init(self, __QVisaDevice__):

		# Extract ini parameters
		_comm = self.get_comm()
		_addr = self.get_addr()

		# Get the port identifier we are trying initialize
		_port = self.get_port()

		# Check if insturement has been initialized in calling application
		if self._config._get_inst_byport(_port) is None:

			# Try to initialize device
			try:

				# Call class constructor
				_inst = __QVisaDevice__(_comm, _addr)

				# Try to call idn.
				try:
					_inst.idn()
					

					# If check_idn() is defined in driver file
					if hasattr(_inst, "check_idn"):

						# If idn checks out, return inst handle
						if _inst.check_idn():

							# Message box to display success
							msg = QMessageBox()
							msg.setIcon(QMessageBox.Information)
							msg.setText("Initialized device at %s"%(_inst.name))
							msg.setWindowTitle("pyVISA Connection")
							msg.setWindowIcon(self.get_icon())
							msg.setStandardButtons(QMessageBox.Ok)
							msg.exec_()
				
							# Add instrument to configuraion object and reset
							self._config._add_inst_handle(_inst)
							self._config._get_inst_byaddr(_addr).reset()
							self.refresh()
									
							# Return insturemnt handle
							return _inst

						else:

							# Message box to display error
							msg = QMessageBox()
							msg.setIcon(QMessageBox.Warning)
							msg.setText("Driver Error: %s is not a %s"%(_port, _inst.type))
							msg.setWindowTitle("pyVISA Error")
							msg.setWindowIcon(self.get_icon())
							msg.setStandardButtons(QMessageBox.Ok)
							msg.exec_()
						
							return None

					# If check_idn() is not defined
					else:

						# Message box to display success
						msg = QMessageBox()
						msg.setIcon(QMessageBox.Information)
						msg.setText("Initialized unverified device at %s"%(_inst.name))
						msg.setWindowTitle("pyVISA Connection")
						msg.setWindowIcon(self.get_icon())
						msg.setStandardButtons(QMessageBox.Ok)
						msg.exec_()
			
						# Add instrument to configuraion object and reset
						self._config._add_inst_handle(_inst)
						self._config._get_inst_byaddr(_addr).reset()
						self.refresh()

						# Return insturemnt handle
						return _inst


				# Timeout here means good write but read error
				except pyvisa.VisaIOError:

					msg = QMessageBox()
					msg.setIcon(QMessageBox.Warning)
					msg.setText("Timeout Error: Device %s initialized but data query failed. Check %s configuration settings. Data termination character should be set to <carriage return><line feed> (\\r\\n)"%(_port, _inst.comm))
					msg.setWindowTitle("pyVISA Error")
					msg.setWindowIcon(self.get_icon())
					msg.setStandardButtons(QMessageBox.Ok)
					msg.exec_()	

					return None


			# Timeout error here means no connection
			except pyvisa.VisaIOError:
				
				# Message box to display error
				msg = QMessageBox()
				msg.setIcon(QMessageBox.Warning)
				msg.setText("Timeout Error: No deivce at %s"%_port)
				msg.setWindowTitle("pyVISA Error")
				msg.setWindowIcon(self.get_icon())
				msg.setStandardButtons(QMessageBox.Ok)
				msg.exec_()

				return None
		
		else:

			# Message box to display error
			msg = QMessageBox()
			msg.setIcon(QMessageBox.Warning)
			msg.setText("Device Error: %s aready initialized"%_port)
			msg.setWindowTitle("pyVISA Error")
			msg.setWindowIcon(self.get_icon())
			msg.setStandardButtons(QMessageBox.Ok)
			msg.exec_()

			return None


	# Set device initialize callback
	def set_init_callback(self, __func__):
		self._init_callback = str(__func__)	

	# Run device initialize callback	
	def _run_init_callback(self):

		if self._init_callback is not None:					
			__func__ = getattr(self._config, self._init_callback)
			__func__()

	# Set the callback for the insturment select combobox
	def set_select_callback(self, __func__):
		self.inst_widget.set_callback(__func__)

