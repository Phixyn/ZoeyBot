"""
samp_query.py - SA-MP query module

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

# SA-MP query module by Erik Sneyders (Lordkire)
#
# Use:
# Create an object server = Server(ip, port)
# Then use server.load()
# If that returns True, the info and players are loaded into the server object
# If it returns False, it couldn't connect to the server
#
# It doesn't get all the information (you can also get weather, gravity, .. but that's not really relevant for a bot).
"""

import socket

def getInt(string, NoB):
    integer = 0
    for i in range(NoB):
        integer += ord(string[i]) << (8*i)
    return integer

class Server(object):
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
       
        #self.loadInfo()
        #self.loadPlayers()

    def loadInfo(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(0.5)
        length = 0
        sip = self.ip.split('.')

        packet = 'SAMP'
        packet += chr(int(sip[0]))
        packet += chr(int(sip[1]))
        packet += chr(int(sip[2]))
        packet += chr(int(sip[3]))
        packet += chr(self.port & 0xFF)
        packet += chr(self.port >> 8 & 0xFF)
        packet += 'i'

        s.sendto(packet, (self.ip, self.port))

        try:
            packet, address = s.recvfrom(1024)
        except:
            return False

        packet = packet[11:]
        self.password = bool(ord(packet[0]))
        packet = packet[1:]
       
        self.playerCount = getInt(packet, 2)
        packet = packet[2:]
       
        self.maxPlayerCount = getInt(packet, 2)
        packet = packet[2:]
       
        length = getInt(packet, 4)
        packet = packet[4:]
        self.hostname = packet[:length]
        packet = packet[length:]
       
        length = getInt(packet, 4)
        packet = packet[4:]
        self.gamemode = packet[:length]
        packet = packet[length:]
       
        length = getInt(packet, 4)
        packet = packet[4:]
        self.map = packet[:length]

        s.close()
        return True

    def loadPlayers(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(0.5)
        length = 0
        playerCount = 0
        self.players = list()
        sip = self.ip.split('.')

        packet = 'SAMP'
        packet += chr(int(sip[0]))
        packet += chr(int(sip[1]))
        packet += chr(int(sip[2]))
        packet += chr(int(sip[3]))
        packet += chr(self.port & 0xFF)
        packet += chr(self.port >> 8 & 0xFF)
        packet += 'd'

        s.sendto(packet, (self.ip, self.port))

        try:
            packet, address = s.recvfrom(1024)
        except:
            return False
       
        packet = packet[11:]
        playerCount = getInt(packet, 2)
        packet = packet[2:]
       
        for i in range(playerCount):
            playerid = getInt(packet, 1)
            packet = packet[1:]

            length = getInt(packet, 1)
            packet = packet[1:]
            nick = packet[:length]
            packet = packet[length:]

            score = getInt(packet, 4)
            packet = packet[4:]

            ping = getInt(packet, 4)
            packet = packet[4:]

            p = Player(playerid, nick, score, ping)
            self.players.append(p)
       
        s.close()
        return True

    def load(self):
        if self.loadInfo() and self.loadPlayers():
            return True
        else:
            return False

class Player(object):
    def __init__(self, playerid, nick, score, ping):
        self.playerid = playerid
        self.nick = nick
        self.score = score
        self.ping = ping
        
