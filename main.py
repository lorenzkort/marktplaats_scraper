"""
Execution of main functions
"""
import logging
from logging.handlers import RotatingFileHandler
import time
from jobs.config.core import LOG_DIR, DATASET_DIR, config
from jobs.channel import check_for_new_listings


# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format=config.log_format,
    datefmt=config.date_time_format,
    handlers=[
        RotatingFileHandler(
            LOG_DIR / 'info.log',
            maxBytes=1048576,
            backupCount=2)
    ])

if __name__ == "__main__":
    while True:
        for channel in config.channels:
            check_for_new_listings(chatId=channel.chatId)
        msg = f"{channel.chatId}: Checked for new listings"
        logging.info(msg)
        print(msg)
        break
        # time.sleep(3600 / config.runs_per_hour)
        