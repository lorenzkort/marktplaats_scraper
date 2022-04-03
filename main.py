"""
Execution of main functions
"""
import logging
import time
from jobs.config.core import LOG_DIR, DATASET_DIR, config
from jobs.channel import check_for_new_listings


# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    filename=LOG_DIR / 'info.log',
    format=config.log_format,
    datefmt=config.date_time_format)

if __name__ == "__main__":
    while True:
        for channel in config.channels:
            check_for_new_listings(chatId=channel.chatId)
            logging.info(f'{channel.chatId}: Checked for new listings')
        time.sleep(3600 / config.runs_per_hour)