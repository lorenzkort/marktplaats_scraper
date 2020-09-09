# import libraries
import urllib.request
import json
import pandas as pd
from telegram_bot import telegram_send_text

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
            print("All items filtered out. No relevant items left for keyword: " + str(keyword) )
    else:
        print("No items found for keyword: " + str(keyword) )
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

# generate url based on keyword, category ID, and Title and Description
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
    dir = '/home/pi/Documents/Python/marktplaatsMaster/data/' #pi
    #dir = '/Users/lorenzkort/Documents/Python/marktplaatsMaster/data/' #mac
    #dir = '/Users/LorenzKort/OneDrive - ITDS Groep B.V/Documenten/GitHub/marktplaats/data/' #windows
    file_name = dir + keyword.replace(' ','_').lower() + '_response.csv'
    query_url = url_gen(keyword, CategoryId, TitleAndDescription)
    items_df = get_items(keyword, query_url) # get items
    notify(items_df, file_name, keyword, chat_id) # Send chat message with new id's
    items_df.to_csv(file_name) # save csv
    return