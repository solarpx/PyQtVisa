# ---------------------------------------------------------------------------------
# 	PyQtVisa -> setup.py
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
import sys

try:
	from setuptools import setup
except ImportError:
	print('Please install or upgrade setuptools or pip to continue')
	sys.exit(1)

setup(name='PyQtVisa',
		description='Qt framework for building PyVISA applications for GPIB, RS232, TCPIP and USB instruments',
		version='1.1.dev5',
		author='Michael Winters',
		author_email="mesoic@protonmail.com",
		url="https://github.com/mesoic/PyQtVisa",
		keywords='Qt VISA GPIB USB serial RS232 measurement acquisition',
		license='MIT License',
		python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*',
		install_requires=['visa', 'matplotlib', 'PyQt5'],
		classifiers=[
			'Development Status :: 5 - Production/Stable',
			'Intended Audience :: Developers',
			'Intended Audience :: Science/Research',
			'License :: OSI Approved :: MIT License',
			'Operating System :: Microsoft :: Windows',
			'Operating System :: POSIX :: Linux',
			'Operating System :: MacOS :: MacOS X',
			'Programming Language :: Python',
			'Topic :: Scientific/Engineering :: Interface Engine/Protocol Translator',
			'Topic :: Software Development :: Libraries :: Python Modules',
			'Programming Language :: Python :: 2',
			'Programming Language :: Python :: 2.7',
			'Programming Language :: Python :: 3',
			'Programming Language :: Python :: 3.4',
			'Programming Language :: Python :: 3.5',
			'Programming Language :: Python :: 3.6',
			'Programming Language :: Python :: 3.7',
			],
		packages=['PyQtVisa', 'PyQtVisa.widgets','PyQtVisa.drivers', 'PyQtVisa.utils'],
		platforms="Linux, Windows, Mac",
		use_2to3=False,
		zip_safe=False,
)