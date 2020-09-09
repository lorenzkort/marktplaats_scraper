from request_item import check, url_gen
from telegram_bot import telegram_send_text
from log_file_handler import app_log
import traceback

# initialize log settings

try:
    if __name__ == "__main__":
        check('Concept 2', '-425371692', '784', TitleAndDescription=True)
        check('Concept2','-425371692', '784',TitleAndDescription=True)
        check('Marzocco', '-367307171')
        check('Anfim', '-367307171')
        check('Mahlkonig', '-367307171')
        check('Mazzer','-367307171')
        check('Fiorenzato', '-367307171')
        #check('Sprinter rolstoel', '-449684046')
        #check('Sprinter rolstoelbus', '-449684046')
        #check('Sprinter invalidebus', '-449684046')
        #check('Sprinter invalide', '-449684046')
        #check('Sprinter personenvervoer', '-449684046')
        #check('Sprinter gehandicapten', '-449684046')
        #check('Sprinter persoonsbus', '-449684046')
        #check('Sprinter personenbus', '-449684046')
except Exception as e:
    app_log.exception(str(e))
    telegram_send_text(str(traceback.format_exc()), '-381451433')
