# ---------------------------------------------------------------------------------
# 	QVisaSaveWidget -> QWidget
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

# Import QT backends
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QLineEdit, QLabel, QFileDialog, QMessageBox

# Helper class to generate save widgets 
class QVisaSaveWidget(QWidget):

	def __init__(self, _app):

		QWidget.__init__(self)

		self._layout = QVBoxLayout()

		# Save note
		self._note_label = QLabel("Measurement Note")
		self._note = QLineEdit()
		self._note.setFixedWidth(200)
		
		# Save button
		self._button = QPushButton("Save Data")
		self._button.clicked.connect(self.gen_data_file)

		# Pack the widget layout
		self._layout.addWidget(_app._gen_hbox_widget([self._note, self._note_label]))
		self._layout.addWidget(self._button)
		self._layout.setContentsMargins(0,0,0,0)

		# Set layout and return the widget
		self.setLayout(self._layout)

		# Cache a reference to the calling application
		self._app = _app

	# Save widget contains the save data method	
	def gen_data_file(self):

		# If data is empty display warning message
		if  self._app._data == {}:

			msg = QMessageBox()
			msg.setIcon(QMessageBox.Warning)
			msg.setText("No measurement data")
			msg.setWindowTitle("Bias Info")
			msg.setWindowIcon(self._app._get_icon())
			msg.setStandardButtons(QMessageBox.Ok)
			msg.exec_()

		# Otherwise save
		else:

			# Inject save note into QVisaDataObject
			self._app._data.add_note( self._note.text() ) 

			# Open file dialog
			dialog = QFileDialog(self)
			dialog.setFileMode(QFileDialog.AnyFile)
			dialog.setViewMode(QFileDialog.Detail)
			filenames = []

			# Select file
			if dialog.exec_():
				filenames = dialog.selectedFiles()


			# Check if filenames is not empty 
			# 	*) for cancel button
			if filenames != []:
				
				self._app._data.write_to_file(filenames[0])

				# Message box to indicate successful save
				msg = QMessageBox()
				msg.setIcon(QMessageBox.Information)
				msg.setText("Measurement data saved")
				msg.setWindowTitle("Application Info")
				msg.setWindowIcon(self._app._get_icon())
				msg.setStandardButtons(QMessageBox.Ok)
				msg.exec_()		


	# Wrapper method for setEnabled 	
	def setEnabled(self, _bool):

		self._button.setEnabled(_bool)
