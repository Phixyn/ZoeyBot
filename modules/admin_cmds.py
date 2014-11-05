"""
admin_cmds.py - Admin commands module

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
from print_data import *

cmdList = ["!msg [channel/nick] [message]", "!join [channel] (channel2) (...)", "!leave (channel) (...)", "!quiet_mode", "!quit"]

def handle_command(bot, data):
	""" Documentation pending. """

	userNick = data[0][1:' '.join(data).find("!")]
	bot.rplChan = data[2]      # Channel to which we will send output, declared in bot.py
	cmd = data[3].lstrip(":")
	params = data[4:] if len(data) > 3 else None  # Obtain command parameters if there are any.

	# cmdList = ["!msg [channel/nick] [message]", "!join [channel] (channel2) (...)", "!leave (channel) (...)", "!quiet_mode", "!quit"]

	if cmd == "!msg" and userNick == bot.OWNER:
		if len(params) != 0:
			bot.send_data("PRIVMSG {0} {1}{2}\r\n".format(params[0], bot.textFormat, ' '.join(params[1:])))
		else:
			bot.send_data("PRIVMSG {0} {1}Usage: !msg [channel/user] [message]\r\n".format(userNick, bot.textFormat))

	elif cmd == "!join" and len(params) != 0 and userNick == bot.OWNER:
		for chan in params:
			bot.join_chan(chan)

	elif cmd == "!leave" and userNick == bot.OWNER:
		if len(params) == 0:
			# Leaves current channel if no channels are specified
			bot.send_data("PART {0}\r\n".format(bot.rplChan))
			if chan in bot.botChannels:
				bot.botChannels.remove(bot.rplChan)

		else:
			for chan in params:
				bot.send_data("PART {0}\r\n".format(chan))
				if chan in bot.botChannels:
					bot.botChannels.remove(chan)
	
	elif cmd == "!quiet_mode" and userNick == bot.OWNER:
		bot.quietMode = True if bot.quietMode == False else False
		echo_data("{0} [ZOEY] Quiet mode has been set to: {1}.".format(utils.timestamp(), bot.quietMode), bot.enableLog)

	elif cmd == "!quit" and userNick == bot.OWNER:
		# To-Do:
		# - Make it accept and handle a /quit reason
		#   + bot.stop(reason) ?
		# - Make it privmsg a random "I'm gonna: " string

		bot.stop()

	elif cmd.lower() == "!help" and len(params) != 0 and params[0] == "admin":
		bot.send_data("PRIVMSG {0} {1}ZoeyBot admin commands:\r\n".format(bot.rplChan, bot.textFormat))
		bot.send_data("PRIVMSG {0} {1}You must be the current bot owner in order to use these.\r\n".format(bot.rplChan, bot.textFormat))
		bot.send_data("PRIVMSG {0} {1}{2}\r\n".format(bot.rplChan, bot.textFormat, ', '.join(cmdList)))

