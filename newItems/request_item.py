# import libraries
import urllib.request
import json
import pandas as pd
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

def notify(df, file_name, keyword, chat_id='-425371692'):
    with open(file_name, 'r') as f:
        for ind in df.index:
            if any(df['id'][ind] in line for line in f):
                pass # known id
            else:
                print('New ' + keyword)
                telegram_send_text('New ' + keyword + ': ' + df['url'][ind], chat_id)
                break
    return

def url_gen(keyword='', CategoryId='', TitleAndDescription=False):
    if keyword != '':
        keyword = str(keyword).replace(' ', '%20')
    if CategoryId != '':
        CategoryId = 'l1CategoryId=' + str(CategoryId)
    if TitleAndDescription == True:
        TitleAndDescription = '&searchInTitleAndDescription=true'
    else:
        TitleAndDescription = ''
    url = 'https://www.marktplaats.nl/lrp/api/search?attributesById[]=32&attributesById[]=31&' + CategoryId + '&limit=100&offset=0&query=' + keyword + TitleAndDescription + '&sortBy=SORT_INDEX&sortOrder=DECREASING'
    return url

def check(keyword='concept 2', chat_id='-425371692', CategoryId='', TitleAndDescription=False):
    pi_dir = '/home/pi/Documents/Python/marktplaatsMaster/data/'
    #mac_dir = '/Users/lorenzkort/Documents/Python/marktplaatsMaster/data/'
    file_name = pi_dir + keyword.replace(' ','_').lower() + '_response.csv'
    query_url = url_gen(keyword, CategoryId, TitleAndDescription)
    items_df = get_items(query_url) # get items
    notify(items_df, file_name, keyword, chat_id) # mail new id's
    items_df.to_csv(file_name) # save csv
    return