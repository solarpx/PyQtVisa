# ---------------------------------------------------------------------------------
# 	QVisaDynamicPlot -> QWidget
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
import random
import numpy as np

# Import QT backends
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QComboBox, QCheckBox, QLabel, QMessageBox,  QSizePolicy
from PyQt5.QtGui import QIcon

# Import matplotlibQT backends
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.ticker import FormatStrFormatter
import matplotlib.pyplot as plt

# Import QVisaColorMap class
from ..utils.QVisaColorMap import QVisaColorMap
from ..utils.QVisaDataObject import QVisaDataObject

# Dynamic plotting library for QVisaApplications
class QVisaDynamicPlot(QWidget):

	def __init__(self, _app):

		QWidget.__init__(self)

		# Axes are be stored in a standard dictionary
		# 	[111]  = subplot(111)
		#	[111t] = subplot(111).twinx()
		self._axes = {}

		# Axes handles will be stored in QVisaDataObject
		#	[111]
		# 		[<key0>] = handles(list)
		# 		[<key1>] = handles(list)
		self._handles = QVisaDataObject()

		# QVisaColorMap class and generator function
		self._cmap = QVisaColorMap()
		self._cgen = self._cmap.gen_next_color()

		# Dictionary to hold plot adjust values
		self._adjust = {'l': 0.15, 'r': 0.90, 't': 0.90, 'b' : 0.10}

		# Generate main layout
		self._gen_main_layout()

		# Cache a reference to the calling application
		self._app = _app
		self.sync = False

	def _gen_main_layout(self):

		self._layout = QVBoxLayout()

		# Generate widgets
		self._gen_mpl_widgets()

		# HBoxLayout for toolbar and clear button
		self._layout_toolbar = QHBoxLayout()	
		self._layout_toolbar.addWidget(self.mpl_toolbar)
		self._layout_toolbar.addWidget(self.mpl_handles_label)
		self._layout_toolbar.addWidget(self.mpl_handles)
		self._layout_toolbar.addWidget(self.mpl_refresh)

		# HBoxLayout for plot object 
		self._layout_plot = QHBoxLayout()
		self._layout_plot.addWidget(self.mpl_canvas)
		
		# Add layouts
		self._layout.addLayout(self._layout_toolbar)
		self._layout.addLayout(self._layout_plot)

		# Set widget layout
		self.setLayout( self._layout )

	# Generate matplotlib widgets	
	def _gen_mpl_widgets(self):
	
		# Generate matplotlib figure and canvas
		self.mpl_figure  = plt.figure(figsize=(8,5))
		self.mpl_canvas  = FigureCanvas(self.mpl_figure)
		self.mpl_toolbar = NavigationToolbar(self.mpl_canvas, self)		

		# Handle selector
		self.mpl_handles_label = QLabel("<b>Show:</b>")
		self.mpl_handles = QComboBox()
		self.mpl_handles.addItem("all-traces")
		self.mpl_handles.setFixedHeight(30)
		self.mpl_handles.currentTextChanged.connect(self.update_visible_handles)

		# Refresh button
		self.mpl_refresh = QPushButton("Clear Data")
		self.mpl_refresh.clicked.connect(self.refresh_canvas)
		self.mpl_refresh.setFixedHeight(32)
		self.mpl_refresh_callback = None

	# Method to enable and disable mpl_refresh button
	def mpl_refresh_setEnabled(self, _bool):
		self.mpl_refresh.setEnabled(_bool)	

	# Add mechanism to pass app method to run on mpl_refresh.clicked
	def set_mpl_refresh_callback(self, __func__):	
		self.mpl_refresh_callback = str(__func__)

	# Run app method attached to mpl_refresh.clicked
	def _run_mpl_refresh_callback(self):	
		if self.mpl_refresh_callback is not None:					
			__func__ = getattr(self._app, self.mpl_refresh_callback)
			__func__()	

	# Sync application data. When True, refresh lines will attempt to 
	# del self._app._data.data[_handle_key] when clearing data in axes 
	# self._handles[_axes_key][_handle_key]. This will synchonize plots
	# with application data.
	def sync_application_data(self, _bool):
		self.sync = _bool

	# Wrapper method to set(change) colormap
	def gen_cmap_colors(self, _cmap="default"):
		self._cmap.gen_cmap_colors(_cmap)

	# Wrapper method to gnertae next color
	def gen_next_color(self):
		return next(self._cgen)

	# Add axes object to widget
	def add_subplot(self, _axes_key=111, twinx=False):

		self._handles.add_key( str(_axes_key) )
		self._axes[str(_axes_key)] = self.mpl_figure.add_subplot(_axes_key)
		
		if twinx:
			self._handles.add_key( str(_axes_key) + 't' )
			self._axes[str(_axes_key)+'t'] = self._axes[str(_axes_key)].twinx()
			

	# Add axes xlabels
	def set_axes_xlabel(self, _axes_key, _xlabel):
		self._axes[_axes_key].set_xlabel( str(_xlabel) ) 

	# Add axes ylabels
	def set_axes_ylabel(self, _axes_key, _ylabel):
		self._axes[_axes_key].set_ylabel( str(_ylabel) ) 

	# Convenience method to set axes labels
	def set_axes_labels(self, _axes_key, _xlabel, _ylabel):
		self.set_axes_xlabel(str(_axes_key), _xlabel)
		self.set_axes_ylabel(str(_axes_key), _ylabel)	

	# Set axes adjust 
	def set_axes_adjust(self, _left, _right, _top, _bottom):
		self._adjust = {'l': _left, 'r': _right, 't': _top, 'b' : _bottom}	

	# Add handle to axes
	def add_axes_handle(self, _axes_key, _handle_key, _color=None):

		# Get handle keys from comboBox
		_handle_keys = [self.mpl_handles.itemText(i) for i in range(self.mpl_handles.count())]

		# Check if handle key is in list
		if _handle_key not in _handle_keys:
			self.mpl_handles.addItem(_handle_key)

		# Add option to set color directly
		if _color is not None:
			h, = self._axes[str(_axes_key)].plot([], [], color=_color)

		# Otherwise generate color on defined map
		else:
			h, = self._axes[str(_axes_key)].plot([], [], color=self.gen_next_color())

		# Add handle to handle keys	
		self._handles.add_subkey(_axes_key, _handle_key)
		self._handles.append_subkey_data(_axes_key, _handle_key, h)

	# Method to get axes handles
	def get_axes_handles(self):
		return self._handles

	# Update axes handle (set)
	def set_handle_data(self, _axes_key, _handle_key, x_data, y_data, _handle_index=0):

		# Get the list of handles
		_h = self._handles.get_subkey_data(_axes_key, _handle_key)

		# Set data values on _handle_index
		_h[_handle_index].set_xdata(x_data)
		_h[_handle_index].set_ydata(y_data)

	# Update axes handle (append)
	def append_handle_data(self, _axes_key, _handle_key, x_value, y_value, _handle_index=0):

		# Get the list of handles
		_h = self._handles.get_subkey_data(_axes_key, _handle_key)

		# Append new values to handle data
		_x = np.append(_h[_handle_index].get_xdata(), x_value)
		_y = np.append(_h[_handle_index].get_ydata(), y_value)

		# Set xdata and ydata to handle
		_h[_handle_index].set_xdata(_x)
		_h[_handle_index].set_ydata(_y)

	# Method to redraw canvas lines
	def update_visible_handles(self):	

		# Get handle
		_show_handle = self.mpl_handles.currentText()
		
		# Set all traces visible
		if _show_handle == "all-traces":

			# For each axis (e.g. 111)
			for _axes_key in self._handles.keys():

				# Check if there are handles on the key 
				if self._handles.subitems(_axes_key) is not None:	

					# Loop through handle_key and handle_list
					for _handle_key, _handle_list in self._handles.subitems(_axes_key):

						[_h.set_visible(True) for _h in _handle_list]
			
		else:

			# For each axis (e.g. 111)
			for _axes_key in self._axes.keys():

				# Check if there are handles on the key 
				if self._handles.subitems(_axes_key) is not None:

					# Loop through handle_key and handle_list
					for _handle_key, _handle_list in self._handles.subitems(_axes_key):

						if _show_handle == _handle_key:

							[_h.set_visible(True) for _h in _handle_list]
													
						else:

							[_h.set_visible(False) for _h in _handle_list]


		self.update_canvas()	

	# Method to update canvas dynamically
	def update_canvas(self):

		# Loop through all figure axes and relimit
		for _key, _axes in self._axes.items():
			_axes.relim()
			_axes.autoscale_view()
			_axes.ticklabel_format(style='sci', scilimits=(0,0), axis='y', useOffset=False)

		# Adjust subplots	
		plt.subplots_adjust(
			left 	= self._adjust['l'], 
			right 	= self._adjust['r'], 
			top  	= self._adjust['t'],
			bottom	= self._adjust['b']
		)
	
		# Draw and flush_events
		self.mpl_canvas.draw()
		self.mpl_canvas.flush_events()

	# Refresh canvas. Note callback will expose args as False
	def refresh_canvas(self, supress_warning=False):
		
		# Only ask to redraw if there is data present
		if (self._handles.keys_empty() == False) and (supress_warning == False):

			msg = QMessageBox()
			msg.setIcon(QMessageBox.Information)
			msg.setText("Clear measurement data (%s)?"%self.mpl_handles.currentText())
			msg.setWindowTitle("QDynamicPlot")
			msg.setWindowIcon(self._app._get_icon())
			msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
			self.msg_clear = msg.exec_()

			if self.msg_clear == QMessageBox.Yes:

				self._run_mpl_refresh_callback()
				self.refresh_lines()
				return True

			else:
				return False

		else:
			
			self._run_mpl_refresh_callback()
			self.refresh_lines()		
			return True


	# Method to delete lines from handle
	def refresh_lines(self):

		# Create empty handle cache
		_del_cache = []

		# For each axes (e.g. 111)
		for _axes_key in self._axes.keys():

			# Check if there are handles on the key 
			if self._handles.subitems(_axes_key) is not None:

				# Loop through handle_key, handle_list objects on axes
				for _handle_key, _handle_list in self._handles.subitems(_axes_key):

					# Check if first handle in the list is visible 
					if _handle_list[0].get_visible() == True and _handle_key not in _del_cache:

						# Cache the handle key for deletion if it has not beed cached yet
						_del_cache.append(_handle_key)
						

		# Loop through cached keys
		for _handle_key in _del_cache:

			# Check for key on each axis (e.g. 111, 111t)
			for _axes_key in self._axes.keys():

				# Remove handles (mpl.Artist obejcts) by calling destructor
				for _handle in self._handles.get_subkey_data(_axes_key, _handle_key):
					_handle.remove()

			# Delete the _handle_key from _handles object
			self._handles.del_subkey(_axes_key, _handle_key)
					
			# Remove _handle_key from dropdown
			self.mpl_handles.removeItem(self.mpl_handles.findText(_handle_key))

			# Remove _handle_key from application data if syncing
			if self.sync == True:
				_data = self._app._get_data_object()
				_data.del_key(_handle_key)


		# If deleting all traces, reset the colormap
		if self.mpl_handles.currentText() == "all-traces":
			self._cmap.gen_reset()

		# Otherwise set text to "all-traces"
		else:
			self.mpl_handles.setCurrentIndex(0)

		# Redraw canvas
		self.update_canvas()


	# Method to reset axes
	def reset_canvas(self):

		# Clear the axes 
		for _key, _axes in self._axes.items():

			# Pull labels
			_xlabel = _axes.get_xlabel()
			_ylabel = _axes.get_ylabel()
			
			# clear axes and reset labels
			_axes.clear()
			_axes.set_xlabel(_xlabel)
			_axes.set_ylabel(_ylabel)

		# Clear registered handles
		# Calling add_key() will re-initialize data dictionary to {} for axes
		[ self._handles.add_key(_axes_key) for _axes_key in self._handles.keys() ]

		# Clear the combobox
		self.mpl_handles.clear()
		self.mpl_handles.addItem("all-traces")

		# Reset the colormap
		self._cmap.gen_reset()

		# Update canvas
		self.update_canvas()
