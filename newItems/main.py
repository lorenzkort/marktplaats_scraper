from request_item import notify_concept2, notify_coffee, notify_fietsen
from telegram_bot import telegram_send_text
from log_file_handler import app_log # initialize log handling settings
import traceback # get error explanation
from run_log import log_this_run

def main():
    try:
        notify_concept2()
        notify_coffee()
        notify_fietsen()
        #check('Sprinter rolstoel', '-449684046')
        #check('Sprinter rolstoelbus', '-449684046')
        #check('Sprinter invalidebus', '-449684046')
        #check('Sprinter invalide', '-449684046')
        #check('Sprinter personenvervoer', '-449684046')
        #check('Sprinter gehandicapten', '-449684046')
        #check('Sprinter persoonsbus', '-449684046')
        #check('Sprinter personenbus', '-449684046')
        log_this_run()

    except Exception as e:
        app_log.exception(str(e))
        telegram_send_text(str(traceback.format_exc()), '-381451433')
        


if __name__ == "__main__":
    main()
    log_this_run()