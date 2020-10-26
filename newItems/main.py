from request_item import notify_concept2
from telegram_bot import telegram_send_text
from log_file_handler import app_log # initialize log handling settings
import traceback # get error explanation
from run_log import log_this_run

def main():
    try:
        notify_concept2()
        log_this_run()
    except Exception as e:
        app_log.exception(str(e))
        telegram_send_text(str(traceback.format_exc()), '-381451433')
    return

if __name__ == "__main__":
    main()