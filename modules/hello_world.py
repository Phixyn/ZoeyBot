"""
hello_world.py - Hello world example module

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

def say_hi():
	""" Prints "Hello world!" """
	print("Hello world!")

def print_modules(bot, data):
	""" Prints a list of modules and whatever is in the variable data """
	print(bot.get_modules())
	print(data)
