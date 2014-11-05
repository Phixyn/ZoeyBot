"""
bot.py - ZoeyBot main class

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
import sys
import socket
import modules.utils as utils
import modules.basic_cmds as basic_cmds
import modules.admin_cmds as admin_cmds
from modules.print_data import *

# make imports better somehow? lol better structure too maybe?!
# or maybe put all commands on single file

class Bot:
	"""
	Main bot class - has all client related funtions such as connect, ping,
	join_chan, etc.

	It also obtains and sorts out the packets we receive, so that
	they can be passed as parameters for other methods in other modules.
	"""

	def __init__(self, HOST, PORT, NICK, SERVPASS, OWNER, *CHANNELS):
		""" Initializes instance variables to be used throughout this class. """

		self.HOST = HOST
		self.PORT = PORT
		self.CHANNELS = list(CHANNELS)
		self.NICK = NICK
		self.SERVPASS = SERVPASS
		self.OWNER = OWNER
		self.IDENT = self.NICK.lower()
		self.REALNAME = "ZoeyBot"

		self.botChannels = []
		self.realHost = HOST
		self.connected = False
		
		self.rplChan = None		# Channel to which commands will send output to. It is declared
								# here since it'll also be used by the reply handler
								# Modules that create new commands should use this variable.
		
		self.quietMode = False
		self.enableDebug = False
		self.enableLog = True

		# self.textFormat = chr(2) + chr(3) + "06"		# Text formatting and color (i.e. bold and purple color)
		self.textFormat = ":" 	# For Twitch.tv
		self.quitReason = "~ ZoeyBot (c) 2012-2014 ~"	# Default quit reason

		# Program information:

		self.script_name = "ZoeyBot - Python IRC Bot"
		self.version_info = "v4.0.0_dev"
		self.author_name = "Phixyn"
		self.author_email = "phixyn@gmail.com"
		self.author_web = "http://phixyn.com"

	def get_modules(self):		
		""" Retrieves all modules and stores them in a list, which it then returns. """

		rootDir = os.getcwd()
		filenames = []
		moduleList = []

		for fn in os.listdir(os.path.join(rootDir, "modules")):
			if fn.endswith(".py") and not fn.startswith("_"):
				filenames.append(os.path.join(rootDir, "modules", fn))
				moduleList.append(os.path.basename(fn)[:-3])       # extract module name from filename

		return moduleList
	
	def send_data(self, sdata):		
		"""
		Sends data to the server and prints it to the console neatly
		using print_data() (found in modules/print_data.py)
		
		sdata - Data to be sent to the server
		"""

		self.sock.send("{0}\r\n".format(sdata))
		print_data(self, sdata.split())
	
	def join_chan(self, chan):
		""" 
		Method used to join a channel on a server. It also
		appends the name of the channel onto a list. A
		check is performed to determine whether we are
		connected to the server (see above, ping_handler).
		"""
		
		if self.connected:
			self.send_data("JOIN {0}\r\n".format(chan))
			if not chan in self.botChannels:
				self.botChannels.append(chan)
	
	def ping_handler(self, data):
		""" Simple method that sends ping replies to the server.
		If the pong was sent successfully, it sets the variable
		"connected" to True.
		
		Note that at the moment, using "connected" to check for
		server connectivity is NOT accurate, as this method
		is not yet finished. It does not handle timeouts and
		other failures that can happen while sending pong.
		"""
		
		self.sock.send("PONG {0}\r\n".format(data[1]))
		self.connected = True

	def serv_reply_handler(self, data):
		""" Documentation pending """
		
		reply_code = data[1]
		
		if reply_code == "242" or reply_code == "250":
			# ----- !stst cmd handler -----
			#
			# self.rplChan works here because the command_handler has set
			# it to the correct channel when !stst was handled
			
			self.send_data("PRIVMSG {0} {1}{2}\r\n".format(self.rplChan, self.textFormat, ' '.join(data[3:]).lstrip(":")))
	
	def command_handler(self, data):
		""" Documentation pending """
		
		cmd = data[3].lstrip(":")
		
		if cmd in basic_cmds.cmdList:
			basic_cmds.handle_command(self, data)
		
		elif cmd in admin_cmds.cmdList:
			admin_cmds.handle_command(self, data)
		
		else:
			echo_data("{0} [INFO] Unknown command: {1}".format(utils.timestamp(), cmd), self.enableLog)
	
	def nickserv_handler(self, data):		
		"""
		Documentation pending
		
		NOTE: This needs MAJOR improvements.
		"""

		# This needs a lot more features!

		# Login handler:
		# - needs improvement!

		if ' '.join(data).find(" :This nickname is registered") != -1:
			print("\n{0} [ZOEY] NickServ is asking for a password for this nickname.".format(utils.timestamp()))
			temp = raw_input("{0} [ZOEY] Please enter your password: ".format(utils.timestamp()))
			print	# Blank line for formatting purposes ('prettying' up stuff...)
			
			self.sock.send("PRIVMSG NickServ identify {0}\r\n".format(temp))
			self.connected = True
		
		# ----- !To Fix! - this code is used two times -----
		for chan in self.CHANNELS:
			self.join_chan(chan)		
	
	def start(self):
		""" Documentation pending """

		# To-Do: 
		# - Info about debug mode (Debug: False)
		# - Same for enableLog
		# - Make showTimestamps

		utils.clear_screen()
		modules = self.get_modules()

		echo_data("\n{0} [ZOEY] ZoeyBot {1} Copyright 2012-2014 (c) {2}".format(utils.timestamp(), self.version_info, self.author_name), self.enableLog)
		echo_data("{0} [ZOEY] This program comes with ABSOLUTELY NO WARRANTY;".format(utils.timestamp()), self.enableLog)
		echo_data("{0} [ZOEY] This is free software, and you are welcome to redistribute it under".format(utils.timestamp()), self.enableLog)
		echo_data("{0} [ZOEY] certain conditions; see the provided license copy for details".format(utils.timestamp()), self.enableLog)

		echo_data("\n{0} [ZOEY] Hello!".format(utils.timestamp()), self.enableLog)
		echo_data("{0} [ZOEY] Loaded modules: {1}.".format(utils.timestamp(), ', '.join(modules)), self.enableLog)
		echo_data("{0} [ZOEY] Print debug messages: {1}.".format(utils.timestamp(), self.enableDebug), self.enableLog)
		echo_data("{0} [ZOEY] Enable logging: {1}.".format(utils.timestamp(), self.enableLog), self.enableLog)
		echo_data("\n{0} [ZOEY] Connecting to {1}:{2} ...\n".format(utils.timestamp(), self.HOST, self.PORT), self.enableLog)
		
		self.connect()

	def stop(self):
		""" Documentation pending """
	
		if self.rplChan and not self.quietMode:
			# If this method was called from a command (e.g. !quit), we probably
			# want to send a farewell message to the channel we were in :)
			self.send_data("PRIVMSG {0} {1}Bye everyone, I'm gonna go eat some binary cupcakes that {2} made me!\r\n".format(self.rplChan, self.textFormat, self.OWNER))

		echo_data("\n{0} [ZOEY] Shutting down...".format(utils.timestamp()), self.enableLog)
		self.sock.send("QUIT :{0}\r\n".format(self.quitReason))
		self.sock.close()
		echo_data("{0} [ZOEY] Closed socket.".format(utils.timestamp()), self.enableLog)
		echo_data("{0} [ZOEY] Bye.\n".format(utils.timestamp()), self.enableLog)
		sys.exit(0)

	def connect(self):
		""" Documentation pending """
		
		readBuffer = ""
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.connect((self.HOST, self.PORT))
		
		if self.SERVPASS:
			# If the server requires a password, send it first
			self.sock.send("PASS {0}\r\n".format(self.SERVPASS))
		
		self.sock.send("NICK {0}\r\n".format(self.NICK))
		self.sock.send("USER {0} {1} {2} :{3}\r\n".format(self.IDENT, self.HOST, self.IDENT, self.REALNAME))

		try:	
			while 1:
				readBuffer = readBuffer + self.sock.recv(1024)
				dataStream = readBuffer.split("\n")
				readBuffer = dataStream.pop()
				
				for self.dataLine in dataStream:
					self.dataLine = self.dataLine.rstrip()
					self.dataLine = self.dataLine.split()
					print_data(self, self.dataLine)

					if self.dataLine[1] == "001":
						# First packet received from an IRC server is usually a 001 command
						# From this, we can get the real hostname of the server
						self.connected = True
						self.realHost = self.dataLine[0].lstrip(":")
			
						# First join on connect
						for chan in self.CHANNELS:
							self.join_chan(chan)
						
					elif self.dataLine[0].lstrip(":") == self.realHost:
						# Any other commands received from the server should also be handled
						self.serv_reply_handler(self.dataLine)
					
					elif self.dataLine[0] == "PING":
						# Handle ping requests
						self.ping_handler(self.dataLine)

					elif self.dataLine[1] == "PRIVMSG" and self.dataLine[3][1] == "!" and len(self.dataLine[3].lstrip(":")) > 1:
						# This is a command
						self.command_handler(self.dataLine)
					
					# TO-DO: chat reply handler, aka AI
					#elif (self.dataLine[1] == "PRIVMSG" or self.dataLine[1] == "JOIN") and self.quietMode == False:
						# self.chat_reply_handler(self.dataLine)
						# modules.chatreply.chat_reply_handler(self.dataLine)
		
					# TO-DO: nickserv handler:
					elif self.dataLine[0][0:' '.join(self.dataLine).find("!")].lstrip(":") == "NickServ":
						# It's a packet from NickServ, call the nickserv handler!
						self.nickserv_handler(self.dataLine)
		
		
		except KeyboardInterrupt as e:
			self.stop()
