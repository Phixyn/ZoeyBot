"""Sets up a logger that logs to file and console."""


__author__ = "Phixyn"


import logging
import os
import sys
import time


LOG_LEVEL = logging.INFO

# Create a Formatter to specify how logging messages are displayed
# e.g. [2017-10-20 02:28:14][INFO] Initializing...
LOG_FORMATTER = logging.Formatter(
    "[%(asctime)s][%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# Set up logger
logger = logging.getLogger()
logger.setLevel(LOG_LEVEL)

# Create and add logging handler for stdout (console) logging
loggerConsoleHandler = logging.StreamHandler(sys.stdout)
loggerConsoleHandler.setFormatter(LOG_FORMATTER)
logger.addHandler(loggerConsoleHandler)

LOGS_FOLDER_NAME = "logs"
LOGS_FOLDER_PATH = os.path.join(os.getcwd(), LOGS_FOLDER_NAME)
# Save log files with the project, date and time in the name
# (e.g. Program-Name_2017-10-20_09-55.log)
LOG_FILE_NAME = time.strftime("ZoeyCord_%Y-%m-%d_%H-%M.log")
LOG_FILE_PATH = os.path.join(LOGS_FOLDER_PATH, LOG_FILE_NAME)

# Create logs folder if it is not present
if not os.path.isdir(LOGS_FOLDER_PATH):
    os.mkdir(LOGS_FOLDER_PATH)

# Create and add logging handler for file logging
loggerFileHandler = logging.FileHandler(LOG_FILE_PATH)
loggerFileHandler.setFormatter(LOG_FORMATTER)
logger.addHandler(loggerFileHandler)


def log_message(message: str):
    """Prints a chat message.

    TODO: log to file, but only to file (already been printed).

    Args:
        message: The chat message to log to the console.
    """
    print(
        "[{0}]{1}".format(
            time.strftime("%Y-%m-%d %H:%M:%S"),
            message
        )
    )
