#!/usr/bin/env python3
"""Entry point for ZoeyCord."""


__author__ = "Phixyn"
__version__ = "0.1.0"


import json
import sys

from util.logging import app_logger
from util.logging import message_logger

import discord


class ZoeyCord(discord.Client):
    async def on_ready(self):
        app_logger.info("Logged in as {0}.".format(self.user))
    
    async def on_message(self, message: str):
        message_logger.info(
            "[#{msg.channel.name}] {msg.author.display_name}: {msg.content}".format(
                msg=message
            )
        )
        if message.author != self.user:
            # Respond to messages received by other users
            if "hello" in message.content.lower():
                channel = client.get_channel(message.channel.id)
                await channel.send("Hello! :3")


def load_config():
    app_logger.debug("Loading config file...")

    config = None
    try:
        with open("config.json", "r") as fob:
            config = json.loads(fob.read())
    except FileNotFoundError as ex:
        app_logger.critical("Config file not present. Please use and modify the example one.")
        sys.exit(1)
    except json.decoder.JSONDecodeError as ex:
        app_logger.critical("Could not parse config file. Please check that it is a valid JSON file.")
        sys.exit(1)

    if not config:
        app_logger.critical("Could not load config file. Please check that it exists and is a valid JSON file.")
        sys.exit(1)

    return config


if __name__ == "__main__":
    config = load_config()
    client = ZoeyCord()
    client.run(config["discord_bot_token"])
