# import libraries
import urllib.request
import json
import pandas as pd
from telegram_bot import telegram_send_text
from request_item import url_gen, get_items

def save_request(keyword, CategoryId='', TitleAndDescription='', filename=''):
    query_url = url_gen(keyword, CategoryId)
    items = get_items(keyword, query_url)
    items.to_csv( 'data/' + filename.replace(' ', '_') + '_resp.csv')
    return

save_request('concept 2', filename='1.csv')
save_request('concept 2', '784', filename='2.csv')
save_request('concept 2', '784', True, filename='3.csv')
save_request('concept 2 roeimachine', '784', True, filename='4.csv')