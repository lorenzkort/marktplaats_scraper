import os
from request_item import notify_concept2, notify_sansui, notify_synths
from telegram_bot import telegram_send_text
from log_file_handler import app_log # initialize log handling settings
import traceback # get error explanation
from run_log import log_this_run

# Change dir name based on operating system
dir_name = os.uname()[0]
if dir_name == 'Darwin':
    dir = '/Users/lorenzkort/Documents/Python/marktplaatsMaster/data/' #mac
elif dir_name == 'Linux':
    dir = '/home/pi/Documents/Python/marktplaatsMaster/data/' #Raspberry Pi
else:
    dir = '/Users/LorenzKort/OneDrive - ITDS Groep B.V/Documenten/GitHub/marktplaats/data/' #windows

def main():
    try:
        notify_concept2()
        notify_sansui()
        notify_synths()
        log_this_run(dir)
    except Exception as e:
        app_log.exception(str(e))
        telegram_send_text(str(traceback.format_exc()), '-381451433')
    return

if __name__ == "__main__":
    main()