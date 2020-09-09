import logging
from logging.handlers import RotatingFileHandler

# initialize the log settings
log_formatter = logging.Formatter('%(asctime)s %(levelname)s %(funcName)s(%(lineno)d) %(message)s')
logFile = 'main_app.log'
my_handler = RotatingFileHandler(logFile, mode='a'
    , maxBytes=5*1024*1024, backupCount=2, encoding=None, delay=0) # Set log file to not exceed 5mb in size
my_handler.setFormatter(log_formatter)
my_handler.setLevel(logging.INFO)
app_log = logging.getLogger('root')
app_log.setLevel(logging.INFO)
app_log.addHandler(my_handler)