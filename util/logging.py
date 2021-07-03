"""Sets up a various loggers that log output to files and console."""


__author__ = "Phixyn"


import logging
import os
import sys
import time


LOG_LEVEL = logging.INFO
LOGS_FOLDER_NAME = "logs"
LOGS_FOLDER_PATH = os.path.join(os.getcwd(), LOGS_FOLDER_NAME)
# Save log files with the project, date and time in the name
# (e.g. Program-Name_2017-10-20_09-55.log)
APP_LOG_FILE_NAME = time.strftime("ZoeyCord_%Y-%m-%d_%H-%M.log")
APP_LOG_FILE_PATH = os.path.join(LOGS_FOLDER_PATH, APP_LOG_FILE_NAME)
MESSAGES_LOG_FILE_NAME = time.strftime("Messages_%Y-%m-%d_%H-%M.log")
MESSAGES_LOG_FILE_PATH = os.path.join(LOGS_FOLDER_PATH, MESSAGES_LOG_FILE_NAME)

# Create a Formatter to specify how log messages are displayed
# e.g. [2017-10-20 02:28:14][INFO] Initializing...
APP_LOG_FORMATTER = logging.Formatter(
    "[%(asctime)s][%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
MESSAGES_LOG_FORMATTER = logging.Formatter(
    "[%(asctime)s]%(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# Create logs folder if it is not present
if not os.path.isdir(LOGS_FOLDER_PATH):
    os.mkdir(LOGS_FOLDER_PATH)

# Set up logger for application and system logs
app_logger = logging.getLogger("app")
app_logger.setLevel(LOG_LEVEL)

# Create and add logging handler for stdout (console) logging
app_logger_console_handler = logging.StreamHandler(sys.stdout)
app_logger_console_handler.setFormatter(APP_LOG_FORMATTER)
app_logger.addHandler(app_logger_console_handler)

# Create and add logging handler for file logging
app_logger_file_handler = logging.FileHandler(APP_LOG_FILE_PATH)
app_logger_file_handler.setFormatter(APP_LOG_FORMATTER)
app_logger.addHandler(app_logger_file_handler)

# Set up logger for chat message logs
message_logger = logging.getLogger("chat_messages")
message_logger.setLevel(LOG_LEVEL)

# Create and add logging handler for stdout (console) logging
message_logger_console_handler = logging.StreamHandler(sys.stdout)
message_logger_console_handler.setFormatter(MESSAGES_LOG_FORMATTER)
message_logger.addHandler(message_logger_console_handler)

# Create and add logging handler for file logging
message_logger_file_handler = logging.FileHandler(MESSAGES_LOG_FILE_PATH)
message_logger_file_handler.setFormatter(MESSAGES_LOG_FORMATTER)
message_logger.addHandler(message_logger_file_handler)
