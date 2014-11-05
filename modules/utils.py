"""
utils.py - Utilities module

ZoeyBot - Python IRC Bot
Copyright 2012-2014 (c) Phixyn

This file is part of ZoeyBot.

ZoeyBot is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

ZoeyBot is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with ZoeyBot. If not, see <http://www.gnu.org/licenses/>.
"""

import os, subprocess
from datetime import datetime as dt

def timestamp():
	""" Documentation pending """

	return dt.strftime(dt.now(), "(%H:%M:%S)")
	
def clear_screen():
	""" Documentation pending """
	# TODO try...except block here maybe?
	
	if (os.name == 'nt'):
		subprocess.call('cls', shell=True)
	
	elif (os.name == 'posix'):
		subprocess.call('clear')
	
	else:
		print(chr(27) + "[2J")

