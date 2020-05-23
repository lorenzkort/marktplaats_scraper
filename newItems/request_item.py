# import json library
import urllib.request
import json
import pandas as pd
from send_mail import mail_data
from telegram_bot import telegram_send_text

def get_items(query_url):
    # get response
    response = urllib.request.urlopen(query_url)
    jresponse = json.load(response)

    # get items
    items = jresponse["listings"]
    base_url = 'https://www.marktplaats.nl'
    for index, item in enumerate(items):
        items[index] = {
            'id': item['itemId'],
            'url': base_url + item['vipUrl'],
            'type': item['priceInfo']['priceType']
        }

    # edit dataframe
    df = pd.DataFrame(items)
    df = df[df['type']!='RESERVED']
    df = df[['id', 'url']]
    return df

def notify(df, file_name, item_name, chat_id='-425371692'):
    with open(file_name, 'r') as f:
        for ind in df.index:
            if any(df['id'][ind] in line for line in f):
                pass # known id
            else:
                print('New ' + item_name)
                telegram_send_text('New ' + item_name + ': ' + df['url'][ind], chat_id)
                break
    return

def check(item_name='concept 2', query_url='https://www.marktplaats.nl/lrp/api/search?l1CategoryId=784&limit=100&offset=0&postcode=2012EG&query=concept%202&sortBy=SORT_INDEX&sortOrder=DECREASING&viewOptions=list-view', chat_id='-425371692'):
    pi_dir = '/home/pi/Documents/Python/marktplaats/'
    mac_dir = ''
    file_name = pi_dir + item_name.replace(' ','_').lower() + '_response.csv'
    items_df = get_items(query_url) # get items
    notify(items_df, file_name, item_name, chat_id) # mail new id's
    items_df.to_csv(file_name) # save csv
    return