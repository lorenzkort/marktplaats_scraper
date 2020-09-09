# import libraries
import urllib.request
import json
import pandas as pd
from telegram_bot import telegram_send_text

def save_request(keyword, CategoryId='', TitleAndDescription='', filename=''):
    query_url = url_gen(keyword, CategoryId)
    items = get_items(keyword, query_url)
    items.to_csv( 'data/' + filename.replace(' ', '_') + '_resp.csv')
    return

'''
save_request('concept 2', filename='1.csv')
save_request('concept 2', '784', filename='2.csv')
save_request('concept 2', '784', True, filename='3.csv')
save_request('concept 2 roeimachine', '784', True, filename='4.csv')
'''

def count_items(keyword, CategoryId='', TitleAndDescription='', filename=''):
    query_url = url_gen(keyword, CategoryId)
    items = get_items(keyword, query_url)
    items_len = len(items)
    print(items_len)
    print(items.tail())
    return

#count_items('concept 2', filename='1.csv')

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
    print(url)
    return url

def get_items(keyword, query_url):
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
            'type': item['priceInfo']['priceType'],
            'sellerId': str(item['sellerInformation']['sellerId'])
        }

    # edit dataframe
    df = pd.DataFrame(items)
    if len(df) > 5: # check if dataframe is not empty
        df = df[df['type']!='RESERVED']
        df = df[df['sellerId']!='25776758'] #filter out thD
        df = df[df['sellerId']!='40684643'] #filter out dlC
        df = df[df['sellerId']!='2085858'] #filter out Mike R
        df = df[df['sellerId']!='19523430'] #filter out Techno Gym faillisement
        df = df[df['sellerId']!='20558893'] #filter out  faillisement
        df = df[['id', 'url']]
        if len(df) > 5:
            pass
        else:
            print("All items filtered out. No relevant items left")
    else:
        print("No items found for keyword: " + str(keyword) )
    return df

query_url = 'https://www.marktplaats.nl/lrp/api/search?attributesById%5B%5D=32&attributesById%5B%5D=31&l1CategoryId=784&limit=100&offset=0&query=concept&sortBy=SORT_INDEX&sortOrder=DECREASING'
response = urllib.request.urlopen(query_url)
jresponse = json.load(response)["listings"]
df = pd.DataFrame(jresponse)
df.to_csv('response.csv')
