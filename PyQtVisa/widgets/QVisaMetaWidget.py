# ---------------------------------------------------------------------------------
# 	QVisaSaveWidget -> QWidget
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
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QLineEdit, QLabel, QMessageBox, QComboBox

# Helper class to generate meta widgets 
class QVisaMetaWidget(QWidget):

	def __init__(self, _app):

		# Init QWidget
		QWidget.__init__(self)

		# Generate main layout
		self.gen_main_layout()

		# Cachee application data
		self._app = _app
		
		# Create subkey (private)
		self._subkey = "__none__"

	# Method to update selected meta item
	def update_meta(self):
		
		# Extract combobox values
		_key = self.meta_keys.currentText()
		_value = self.meta_value.text()
		
		# Set metadata for key. 
		if _key is not "":

			self._app.set_metadata(_key, self._subkey, _value)

			# Tell user that description has been added 
			msg = QMessageBox()
			msg.setIcon(QMessageBox.Warning)
			msg.setText("Metadata Updated")
			msg.setWindowTitle("PyQtVisa Info")
			msg.setWindowIcon(self._app._get_icon())
			msg.setStandardButtons(QMessageBox.Ok)
			msg.exec_()


	# Method to update QLineEdit on key changed
	def update_value_field(self):

		# Extract combobox value. If the keylist is empty, this 
		# will return an empty string
		_key = self.meta_keys.currentText()

		# Check if the key list is empty
		if _key != "":

			_meta = self._app.get_metadata(_key, self._subkey)

			# Check if meta is not none
			if _meta is not None:
				
				self.meta_value.setText(str(_meta))

			else:
				
				self.meta_value.setText("")		

	# Method to get keys out of widget
	def get_meta_keys(self):
		return [self.meta_keys.itemText(i) for i in range(self.meta_keys.count())]		

	# Method to set meta subkey	
	def set_meta_subkey(self, _subkey):
		self._subkey = _subkey

	# Method to add key to meta
	def add_meta_key(self, key):

		# Dont trigger textChanged callback on key add
		self.meta_keys.blockSignals(True)
		self.meta_keys.addItem(key)
		self.meta_keys.setCurrentText(key)
		self.meta_keys.blockSignals(False)

		# Set metavalue for new key to empty string
		self.meta_value.setText("")

	# Method to delete meta key
	def del_meta_key(self, key):
		self.meta_keys.removeItem(self.meta_keys.findText(key))	

	# Method to generate main layout
	def gen_main_layout(self):

		self.meta_keys = QComboBox() 
		self.meta_keys.setFixedHeight(30)
		self.meta_keys.currentTextChanged.connect(self.update_value_field)

		self.meta_value = QLineEdit()
		self.meta_value.setFixedHeight(30)


		self.meta_submit = QPushButton("Add")
		self.meta_submit.setFixedHeight(30)
		self.meta_submit.clicked.connect(self.update_meta)

		self.layout = QHBoxLayout()  
		self.layout.addWidget(self.meta_submit,1)
		self.layout.addWidget(self.meta_keys, 1)
		self.layout.addWidget(self.meta_value, 2)
		self.layout.setContentsMargins(0,0,0,0)

		self.setLayout(self.layout)
