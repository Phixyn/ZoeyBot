#!/usr/bin/env python3
"""Entry point for ZoeyCord."""


__author__ = "Phixyn"
__version__ = "0.1.0"


import json
import sys
from util.logging import log_message
from util.logging import logger

import discord


class ZoeyCord(discord.Client):
    async def on_ready(self):
        logger.info("Logged in as {0}.".format(self.user))
    
    async def on_message(self, message: str):
        log_message(
            "[#{msg.channel.name}] {msg.author.nick}: {msg.content}".format(
                msg=message
            )
        )
        if message.author != self.user:
            # Respond to messages received by other users
            if "hello" in message.content.lower():
                channel = client.get_channel(message.channel.id)
                await channel.send("Hello! :3")


def load_config():
    logger.debug("Loading config file...")

    config = None
    try:
        with open("config.json", "r") as fob:
            config = json.loads(fob.read())
    except FileNotFoundError as ex:
        logger.critical("Config file not present. Please use and modify the example one.")
        sys.exit(1)
    except json.decoder.JSONDecodeError as ex:
        logger.critical("Could not parse config file. Please check that it is a valid JSON file.")
        sys.exit(1)

    if not config:
        logger.critical("Could not load config file. Please check that it exists and is a valid JSON file.")
        sys.exit(1)

    return config


if __name__ == "__main__":
    config = load_config()
    client = ZoeyCord()
    client.run(config["bot_token"])
