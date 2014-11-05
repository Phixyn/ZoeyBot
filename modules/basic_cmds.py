"""
basic_cmds.py - Basic commands module 

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

from random import randint
import samp_query

cmdList = ["!help", "!hello", "!ping", "!dice", "!stst", "!bot_chans", "!bot_info", "!bot_owner", "!samp", "!samp-pl"]

def handle_command(bot, data):
	""" Documentation pending """

	userNick = data[0][1:' '.join(data).find("!")]
	bot.rplChan = data[2]		# Channel to which we will send output, declared in bot.py
	cmd = data[3].lstrip(":")
	params = data[4:] if len(data) > 3 else None	# Obtain command parameters if there are any.

	# cmdList = ["!help", "!hello", "!ping", "!dice", "!stst", "!bot_chans", "!bot_info", "!bot_owner"]

	# ----- Commands: -----

	if cmd == "!hello":
		bot.send_data("PRIVMSG {0} {1}Hello {2}! (:\r\n".format(bot.rplChan, bot.textFormat, userNick))

	elif cmd == "!ping":
		bot.send_data("PRIVMSG {0} {1}Pong! (:\r\n".format(bot.rplChan, bot.textFormat))

	elif cmd == "!dice":
		bot.send_data("PRIVMSG {0} {1}{2} rolls a six-sided dice. It lands on {3}.\r\n".format(bot.rplChan, bot.textFormat, userNick, randint(1,6)))

	elif cmd == "!stst":
		# Handled by bot.serv_reply_handler()
		# - Hence we don't use send_data() here,
		#   but in serv_reply_handler() instead. 

		bot.sock.send("STATS uptime\r\n")
		#bot.sock.send("STATS\r\n")
	
	elif cmd == "!bot_chans":
		bot.send_data("PRIVMSG {0} {1}I'm in channels: {2}\r\n".format(bot.rplChan, bot.textFormat, ', '.join(bot.botChannels)))

	elif cmd == "!bot_owner":
		bot.send_data("PRIVMSG {0} {1}My owner is {2}.\r\n".format(bot.rplChan, bot.textFormat, bot.OWNER))

	elif cmd == "!bot_info":
		bot.send_data("PRIVMSG {0} {1}{2}\r\n".format(bot.rplChan, bot.textFormat, ("-"*35)))
		bot.send_data("PRIVMSG {0} {1}{2}\r\n".format(bot.rplChan, bot.textFormat, bot.script_name))
		bot.send_data("PRIVMSG {0} {1}{2}\r\n".format(bot.rplChan, bot.textFormat, ("-"*35)))
		bot.send_data("PRIVMSG {0} {1}Version: {2}\r\n".format(bot.rplChan, bot.textFormat, bot.version_info))
		bot.send_data("PRIVMSG {0} {1}Author: {2} ({3})\r\n".format(bot.rplChan, bot.textFormat, bot.author_name, bot.author_email))
		bot.send_data("PRIVMSG {0} {1}Website: {2}\r\n".format(bot.rplChan, bot.textFormat, bot.author_web))
	
	elif cmd.lower() in ("!help", "!commands", "!cmds") and len(params) == 0:
		bot.send_data("PRIVMSG {0} {1}ZoeyBot help commands:\r\n".format(bot.rplChan, bot.textFormat))
		bot.send_data("PRIVMSG {0} {1}!help admin, !help basic, !help samp\r\n".format(bot.rplChan, bot.textFormat))

	elif cmd.lower() == "!help" and len(params) != 0 and params[0] == "basic":
		bot.send_data("PRIVMSG {0} {1}Basic commands:\r\n".format(bot.rplChan, bot.textFormat))
		bot.send_data("PRIVMSG {0} {1}{2}\r\n".format(bot.rplChan, bot.textFormat, ', '.join(cmdList)))

	elif cmd.lower() == "!help" and len(params) != 0 and params[0] == "samp":
		bot.send_data("PRIVMSG {0} {1}SA-MP Query Mechanism commands\r\n".format(bot.rplChan, bot.textFormat))
		bot.send_data("PRIVMSG {0} {1}Allows you to query a San Andreas Multiplayer server.".format(bot.rplChan, bot.textFormat))
		bot.send_data("PRIVMSG {0} {1}!samp [server IP] [server PORT], !samp-pl [server IP] [server PORT]\r\n".format(bot.rplChan, bot.textFormat))
	
	# SA-MP (GTA: San Andreas Multiplayer) Query commands.
	# Requires the SA-MP Query module by Lordkire.
	# TODO Maybe move this to the SAMPQuery module?

	elif cmd == "!samp":
		if len(params) < 2:
			bot.send_data("PRIVMSG {0} {1}Usage: !samp (server IP) (server PORT)\r\n".format(userNick, bot.textFormat))

		elif len(params[0].split(".")) != 4:
			# Checking if IP is in a valid format:
			bot.send_data("PRIVMSG {0} {1}ERROR: First argument must be a valid IP address.\r\n".format(userNick, bot.textFormat))

		else:
			IP = params[0]
			PORT = int(params[1])
			server = samp_query.Server(IP, PORT)
			
			# Attempt to query server:
			if server.load():
				bot.send_data("PRIVMSG {0} {1}Queried {2}:{3} successfully.\r\n".format(userNick, bot.textFormat, IP, PORT))
				bot.send_data("PRIVMSG {0} {1}{2}\r\n".format(userNick, bot.textFormat, ("-"*40)))
				bot.send_data("PRIVMSG {0} {1}Hostname: {2}".format(userNick, bot.textFormat, server.hostname))
				bot.send_data("PRIVMSG {0} {1}Players: {2}/{3}".format(userNick, bot.textFormat, server.playerCount, server.maxPlayerCount))
				bot.send_data("PRIVMSG {0} {1}Gamemode: {2}".format(userNick, bot.textFormat, server.gamemode))
				bot.send_data("PRIVMSG {0} {1}Map: {2}".format(userNick, bot.textFormat, server.map))
				bot.send_data("PRIVMSG {0} {1}Password required: {2}.".format(userNick, bot.textFormat, server.password))
				bot.send_data("PRIVMSG {0} {1}{2}\r\n".format(userNick, bot.textFormat, ("-"*40)))
				bot.send_data("PRIVMSG {0} {1}Use !samp-pl to show player list.".format(userNick, bot.textFormat))

			else:
				bot.send_data("PRIVMSG {0} {1}Could not query SA-MP server at {2}:{3}\r\n".format(userNick, bot.textFormat, IP, PORT))
	
	elif cmd == "!samp-pl":		
		if len(params) < 2:
			bot.send_data("PRIVMSG {0} {1}Usage: !samp-pl (server IP) (server PORT)\r\n".format(userNick, bot.textFormat))

		elif len(params[0].split(".")) != 4:
			bot.send_data("PRIVMSG {0} {1}ERROR: First argument must be a valid IP address.\r\n".format(userNick, bot.textFormat))

		else:
			server  = samp_query.Server(params[0], int(params[1]))
			if server.load():
				bot.send_data("PRIVMSG {0} {1}List of online players at {2}:{3}:\r\n".format(userNick, bot.textFormat, params[0], params[1]))
				bot.send_data("PRIVMSG {0} {1}{2}\r\n".format(userNick, bot.textFormat, ("-"*40)))
				bot.send_data("PRIVMSG {0} {1} (ID) Name\r\n".format(userNick, bot.textFormat))

				for player in server.players:
					bot.send_data("PRIVMSG {0} {1} ({2}) {3}\r\n".format(userNick, bot.textFormat, player.playerid, player.nick))

				bot.send_data("PRIVMSG {0} {1}{2}\r\n".format(userNick, bot.textFormat, ("-"*40)))
				bot.send_data("PRIVMSG {0} {1}End.\r\n".format(userNick, bot.textFormat))

			else:
				bot.send_data("PRIVMSG {0} {1}Could not query SA-MP server at {2}:{3}\r\n".format(userNick, bot.textFormat, params[0], params[1]))

