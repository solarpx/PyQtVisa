# ---------------------------------------------------------------------------------
# 	QVisaDeviceControl -> QWidget
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
from .QVisaDeviceSelect import QVisaDeviceSelect
from .QVisaResourceList import QVisaResourceList

# This widget provides a mechanism to initialize QVisaDevice objects in the 
# context of a QVisaConfigure object.
class QVisaDeviceControl(QWidget):

	def __init__(self, _config):

		# Call QWidget init
		QWidget.__init__(self)

		# Cache calling QVisaConfigure object
		self._config = _config

		# Generate main layout
		self.gen_main_layout()

		# Callbacks 
		self._init_callback = None
		self._device_select_callback = None

	def gen_main_layout(self):
	
		# Create configuration layout
		self.layout = QVBoxLayout()

		# Initialize device button
		self.init_button = QPushButton("Initialize Device")
		self.init_button.clicked.connect(self._run_init_callback)
		
		# Generate resource list widget
		self.resource_list = QVisaResourceList(self._config)

		# Generate insturment selector	
		self.device_select_label = QLabel("<b>Initialized Devices</b>")
		self.device_select = QVisaDeviceSelect(self._config)

		# Configuration selector
		self.layout.addWidget(self.init_button)
		self.layout.addWidget(self.resource_list)
		self.layout.addWidget(self.device_select_label)
		self.layout.addWidget(self.device_select)

		self.setLayout(self.layout)

	# Mode select widget
	def gen_conf_widget(self):
		
		# Generate widget
		self.comm_widget = self.gen_comm_widget()		

		# Address spinbox and button as pags
		self.comm_pages = QStackedWidget()
	
		# Pack widgets into QHBoxLayout
		self.conf_layout = QHBoxLayout()
		self.conf_layout.addWidget(self.comm_widget)
		self.conf_layout.setContentsMargins(0,0,0,0)

		# Create widget, set layout, and return
		self.conf_widget = QWidget()
		self.conf_widget.setLayout(self.conf_layout)
		return self.conf_widget

	# Method to get current insturemnt
	def get_current_device(self):

		_name = self.device_select.currentText() 
		Device = self._config.get_device_by_name(_name)

		if Device is not None:
			return Device

		else: 
			return None

	def get_icon(self):

		try :
			return self._config._icon
		except: 
			return QIcon()

	# Refresh device select widget
	def refresh(self):
		self.device_select.blockSignals(True)
		self.device_select.refresh( self._config )
		self.device_select.blockSignals(False)

	# initalize Insturment
	def init(self, __QVisaDevice__):

		# Check if insturement has been initialized in calling application
		_resource = self.resource_list.get_current_device()

		if self._config.get_device(_resource) is None:

			# Try to initialize device
			try:

				# Call class constructor
				Device = __QVisaDevice__(_resource)

				# Try to call idn.
				try:

					# Timeout here means good write but read error
					Device.idn()

					# If check_idn() is defined in driver file
					if hasattr(Device, "check_idn"):

						# If idn checks out, return inst handle
						if Device.check_idn():

							# Message box to display success
							msg = QMessageBox()
							msg.setIcon(QMessageBox.Information)
							msg.setText("Initialized device at %s"%(Device.get_property("name")))
							msg.setWindowTitle("pyVISA Connection")
							msg.setWindowIcon(self.get_icon())
							msg.setStandardButtons(QMessageBox.Ok)
							msg.exec_()
				
							# Add instrument to configuraion object and reset
							self._config.add_device(Device)
							self.refresh()
									
							# Return insturemnt handle
							Device.rst()
							return Device

						else:

							# Message box to display error
							msg = QMessageBox()
							msg.setIcon(QMessageBox.Warning)
							msg.setText("Driver Error: %s is not a %s"%(_resource, Device.get_property("type")))
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
						msg.setText("Initialized unverified device at %s"%(Device.get_property("name")))
						msg.setWindowTitle("pyVISA Connection")
						msg.setWindowIcon(self.get_icon())
						msg.setStandardButtons(QMessageBox.Ok)
						msg.exec_()
			
						# Add instrument to configuraion object and reset
						self._config.add_device(Device)
						self.refresh()
									
						# Return insturemnt handle
						Device.rst()
						return Device
				
				except UnicodeDecodeError:

					# Message box to display error
					msg = QMessageBox()
					msg.setIcon(QMessageBox.Warning)
					msg.setText("Driver Error: %s is not a %s"%(_resource, Device.get_property("type")))
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
				msg.setText("Timeout Error: No deivce at %s"%(_resource))
				msg.setWindowTitle("pyVISA Error")
				msg.setWindowIcon(self.get_icon())
				msg.setStandardButtons(QMessageBox.Ok)
				msg.exec_()

				return None
		
		else:

			# Message box to display error
			msg = QMessageBox()
			msg.setIcon(QMessageBox.Warning)
			msg.setText("Device Error: %s aready initialized"%(_resource))
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
		self.device_select.set_callback(__func__)

