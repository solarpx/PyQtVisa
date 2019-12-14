# ---------------------------------------------------------------------------------
#	QVisaColorMap 
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
import numpy as np

# Import matplotlib colormaps
import matplotlib.cm as cm

# A utility class to wrap the matplotlib colormap class. QVisaColorMap provides an 
# easy programmartice interface for interacting with mpl colormaps in dynamic plots. 
# This class can also be imported into other programs and used as a stand-alone class
# for scientific plotting
class QVisaColorMap:

	def __init__(self):

		# Generate base colormap
		self.gen_cmap_colors("default")

	# Get colormap
	def get_cmap(self):
		return self.cmap		

	# Get colors
	def get_colors(self):
		return self.colors

	# Method to generate color base	
	def gen_cmap_colors(self, _cmap="base", _ncolors=16):

		# Base colormap
		if _cmap == "base":
			self.cmap    = None
			self.colors  = ['b', 'g', 'r', 'c', 'm', 'y', 'k']

		# Tableau colormap	
		elif _cmap in ["tableau", "default"]:
			
			self.colors = [
				'tab:blue', 
				'tab:orange', 
				'tab:green', 
				'tab:red', 
				'tab:purple', 
				'tab:brown', 
				'tab:pink', 
				'tab:gray', 
				'tab:olive', 
				'tab:cyan'
			]

		# Generate colors on any other mpl colormap
		else:
			self.cmap = cm.get_cmap(_cmap)
			self.colors = [ self.cmap(_) for _ in np.linspace(0, 1, _ncolors) ]

	# Generator function for colors
	def gen_next_color(self):

		index = -1
		while True:
			index += 1
			yield self.colors[ index % len(self.colors) ]	
