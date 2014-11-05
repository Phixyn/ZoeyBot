"""
print_data.py - print_data module

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

import os
import utils

logFile = os.path.join(os.getcwd(), "bot_log.txt")
logFile_raw = os.path.join(os.getcwd(), "bot_log_debug.txt")

def log_data(data, debug=False):
	""" Documentation pending """
	
	# logFile = os.path.join(os.getcwd(), "bot_log.txt")
	# logFile_raw = os.path.join(os.getcwd(), "bot_log_raw.txt")

	# Checks if the log files are present - if not, they will be created	
	for fn in (logFile, logFile_raw):
		if not os.path.exists(fn) or not os.path.isfile(fn):
			fob = open(fn, "w")
			fob.close()

	# Log dat data
	if debug == False:
		fob = open(logFile, "a")
	else:
		fob = open(logFile_raw, "a")
	fob.writelines("{0}\n".format(data))
	fob.close()

def echo_data(msg, log):
	"""
	msg - The message to be printed and/or logged.
	log - bot.enableLog var should be passed here
		  this is used to determine whether or not
          data should be logged as well as printed.
	"""

	print(msg)
	if log == True: log_data(msg)

def print_data(bot, data):
	""" 
	Prints data to the console according to the type of data
	received. If it is debug mode (debug=True), it will print all
	data raw as it receives it.

	cmsg = Console message - message to be printed and/or logged
	
	In some cases we use if(data[0] == "PACKET")
	This is to figure out if that data is being sent by us
	When we send data, the packet name comes in first
	This allows us to handle and print data as we send it using
	send_data() in ../bot.py
	
	If we just passed sent data to this function it would print
	it in a very awkward way since it wouldn't know how to handle
	the different format of sent data (wherein packet names come
	first). In received data, generally the sender name/hostname
	comes first.
	"""

	if bot.enableDebug == True:
		# Are we on debug mode? Print everything!
		cmsg = "{0} [Debug] {1}".format(utils.timestamp(), ' '.join(data))
		print(cmsg)
		if bot.enableLog == True: log_data(cmsg, debug=True)
	
	else:
		# We're not debugging, just print stuff neatly :)

		if data[0] == ":"+bot.realHost:
			# Print server info messages
			echo_data("{0} [SERVER] {1}".format(utils.timestamp(), ' '.join(data[3:]).lstrip(":")), bot.enableLog)

		elif ' '.join(data).find("PRIVMSG") != -1:
			# Print chat messages
			user = data[0][1:' '.join(data).find("!")]
			channel = data[2]
			msg = ' '.join(data[3:]).lstrip(":")
			
			if channel == bot.NICK:
				# Handler for Private Messages we receive from other users
				echo_data("{0} [PM from {1}] {2}".format(utils.timestamp(), user, msg), bot.enableLog)

			elif data[0] == "PRIVMSG" and data[1][0] != "#":
				# Handler for Private Messages we (the bot) send to other users
				echo_data("{0} [PM to {1}] {2}".format(utils.timestamp(), data[1], ' '.join(data[2:]).lstrip(":")), bot.enableLog)

			elif data[0] == "PRIVMSG":
				# Handler for messages we (the bot) send
				echo_data("{0} [{1}] {2}: {3}".format(utils.timestamp(), data[1], bot.NICK, ' '.join(data[2:]).lstrip(":")), bot.enableLog)

			else:
				# Handler for every other message
				echo_data("{0} [{1}] {2}: {3}".format(utils.timestamp(), channel, user, msg), bot.enableLog)

		# Handlers for printing joining/leaving messages and quit messages:
		# TO-DO
		# - Maybe replace ' '.join(data).find with a var?

		elif ' '.join(data).find("JOIN") != -1:
			if data[0] == "JOIN":
				echo_data("{0} [INFO] You have joined the channel: {1}".format(utils.timestamp(), data[1].lstrip(":")), bot.enableLog)
			
			else:	
				echo_data("{0} [{1}] {2} has joined the channel.".format(utils.timestamp(), data[2].lstrip(":"), data[0][1:' '.join(data).find("!")]), bot.enableLog)

		elif ' '.join(data).find("PART") != -1:			
			if data[0] == "PART":
				echo_data("{0} [INFO] You have left the channel: {1}".format(utils.timestamp(), data[1].lstrip(":")), bot.enableLog)
			
			else:
				echo_data("{0} [{1}] {2} has left the channel.".format(utils.timestamp(), data[2].lstrip(":"), data[0][1:' '.join(data).find("!")]), bot.enableLog)

		elif ' '.join(data).find("QUIT") != -1:
			echo_data("{0} [INFO] {1} has left. (reason: {2})".format(utils.timestamp(), data[0][1:' '.join(data).find("!")], ' '.join(data[2:]).lstrip(":")), bot.enableLog)

		elif ' '.join(data).find("MODE") != -1:
			# Mode change
			if len(data) == 4:
				# Mode set on join
				echo_data("{0} [INFO] Your mode has been set to: {1}".format(utils.timestamp(), data[3].lstrip(":")), bot.enableLog)

			elif data[0][1:' '.join(data).find("!")] == data[4]:
				# User setting their own mode
				echo_data("{0} [{1}] {2} has changed their mode to: {3}".format(utils.timestamp(), data[2], data[0][1:' '.join(data).find("!")], data[3]), bot.enableLog)

			elif data[4] == bot.NICK:
				# Someone sets your bot's mode:
				echo_data("{0} [{1}] {2} has changed your mode to: {3}".format(utils.timestamp(), data[2], data[0][1:' '.join(data).find("!")], data[3]), bot.enableLog)

			else:
				echo_data("{0} [{1}] {2} has changed {3}'s mode to: {4}".format(utils.timestamp(), data[2], data[0][1:' '.join(data).find("!")], data[4], data[3]), bot.enableLog)

		elif ' '.join(data).find("NICK") != -1:
			# User changed name
			oldNick = data[0][1:' '.join(data).find("!")]
			newNick = data[2].lstrip(":")
			echo_data("{0} [INFO] {1} has changed their name to {2}.".format(utils.timestamp(), oldNick, newNick), bot.enableLog)
	
		elif ' '.join(data).find("KICK") != -1:
			
			# If the reason received is the same as the person kicking, then no reason was specified
			# and therefore should be blank
			reason = ' '.join(data[4:]).lstrip(":") if data[4] != data[0][1:' '.join(data).find("!")] else ""

			if data[3] == bot.NICK:
				# Your bot was kicked from the channel
				echo_data("{0} [{1}] You have been kicked from the channel by {2}. (reason: {3})".format(utils.timestamp(), data[2], data[0][1:' '.join(data).find("!")], reason), bot.enableLog)

			else:
				# Someone else was kicked
				echo_data("{0} [{1}] {2} has been kicked from the channel by {3}. (reason: {4})".format(utils.timestamp(), data[2], data[3], data[0][1:' '.join(data).find("!")], reason), bot.enableLog)

		elif ' '.join(data).find("TOPIC") != -1:
			# Topic was set or changed
			echo_data("{0} [{1}] {2} has changed the topic to: {3}".format(utils.timestamp(), data[2], data[0][1:' '.join(data).find("!")], ' '.join(data[3:]).lstrip(":")), bot.enableLog)

		elif ' '.join(data).find("PING") != -1:
			# echo_data("{0} [INFO]: Server ping, sending response.".format(utils.timestamp()), bot.enableLog)
			pass	# Don't print ping messages

		else:
			echo_data("{0} [INFO] {1}".format(utils.timestamp(), ' '.join(data).lstrip(":")), bot.enableLog)
		
