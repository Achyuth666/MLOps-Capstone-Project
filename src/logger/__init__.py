import logging
import os
from logging.handlers import RotatingFileHandler
from datetime import datetime
import sys


# constants for logginf configuration
LOG_DIR = "logs"
LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"
MAX_LOG_SIZE = 5*1024*1024 #5MB
BACKUP_COUNT = 3 #number of backup log files to keep

# construct the log file path
root_dir = os.path.dirname(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
log_dir_path = os.path.join(root_dir, LOG_DIR)
os.makedirs(log_dir_path, exist_ok=True)
log_file_path = os.path.join(log_dir_path, LOG_FILE)

def configure_logger():
    '''
    configures logging with a rotating file handler adn a console handler
    '''
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter("[%(asctime)s] %(name)s - %(levelname)s - %(message)s")

    # FILE HANDLER
    file_handler = RotatingFileHandler(log_file_path, maxBytes=MAX_LOG_SIZE, backupCount=BACKUP_COUNT, encoding="utf-8")
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)

    # CONSOLE HANDLER
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.INFO)

    # ADD HANDLERS TO THE LOGGER
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

configure_logger()

