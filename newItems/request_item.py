import os
import copy
from datetime import datetime, timedelta
import time
import unicodedata
import requests
import json
import pandas as pd
from telegram_bot import telegram_send_text
from request import get_request

now = datetime.utcnow() + timedelta(hours=2)

# Change dir name based on operating system
dir_name = os.uname()[0]
if dir_name == 'Darwin':
    dir = '/Users/lorenzkort/Documents/Python/marktplaatsMaster/data/' #mac
elif dir_name == 'Linux':
    dir = '/home/pi/Documents/Python/marktplaatsMaster/data/' #Raspberry Pi
else:
    dir = '/Users/LorenzKort/OneDrive - ITDS Groep B.V/Documenten/GitHub/marktplaats/data/' #windows

# gets all items from an API-url with the paired keyword
def get_items(keyword, query_url):
    # get listings from Marktplaats API
    response = get_request(query_url)
    items = response.json()["listings"]

    # set base url from Marktplaats
    print('Before importing: ',len(items))
    base_url = 'https://www.marktplaats.nl'

    # filter listings to relevant information
    for index, item in enumerate(items):

        # try converting response to the right values
        try:
            advertType = item['traits'][0]
        except IndexError:
            advertType = None
        try:
            price = float(item['priceInfo']['priceCents'])
            if price > 0:
                price = price / 100
            else:
                price = 'NaN'
        except Exception as e:
            print(e)
            price = 'NaN'
        try:
            distance = float(item['location']['distanceMeters'])
            if distance > 0:
                distance = distance / 1000
            else:
                distance = '0'
        except:
            distance = '0'
        
        items[index] = {
            'id': item['itemId'],
            'title': item['title'],
            'url': base_url + item['vipUrl'],
            'bidType': item['priceInfo']['priceType'],
            'price': price,
            'sellerId': str(item['sellerInformation']['sellerId']),
            'advertType': advertType,
            'distance': distance,
            'city': item['location']['cityName']
        }

    # filter dataframe based on advertisement type and user ID
    df = pd.DataFrame(items)
    if len(df) > 0: # check if dataframe is not empty
        df = df[df['advertType']== 'PACKAGE_FREE']
        df = df[df['sellerId']!='25776758'] #filter out thD
        df = df[df['sellerId']!='40684643'] #filter out dlC
        df = df[df['sellerId']!='2085858'] #filter out Mike R
        df = df[df['sellerId']!='19523430'] #filter out Techno Gym faillisement
        df = df[df['sellerId']!='20558893'] #filter out  faillisement
        if len(df) > 0:
            print('After filtering: ',len(df))
        else:
            print("All items filtered out. No relevant items left for keyword: " + str(keyword) )
    else:
        print("No items found for keyword: " + str(keyword) )
    
    return df

# check wether a dataframe has new items compared to saved dataframe in file
def get_new_items(new_df, file_name, keyword):
    try:
        old_df = pd.read_csv(file_name) #try getting file
    except:
        old_df = copy.deepcopy(new_df) #if file does not exist, use new df as dummy
    old_df = old_df[['id','url']]
    new_df = new_df
    new_items = new_df.assign(Inold_df=new_df.url.isin(old_df.url).astype(int))
    new_items = new_items[new_items['Inold_df']==0]
    return new_items

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
    url = 'https://www.marktplaats.nl/lrp/api/search?' + CategoryId + '&limit=100&offset=0&postcode=2012EG&query=' + keyword + TitleAndDescription + '&sortBy=SORT_INDEX&sortOrder=DECREASING'    
    return url

def check_new_items(keyword='concept 2', chat_id='-425371692', CategoryId='', TitleAndDescription=False):
    # create filename and base url
    file_name = dir + keyword.replace(' ','_').lower() + '_response.csv'
    query_url = url_gen(keyword, CategoryId, TitleAndDescription)
    
    # Scroll through pages untill not items are left
    item_list = []
    offset = 0
    while True:
        page = get_items(keyword, query_url.replace('offset=0','offset=' + str(offset)))
        if len(page) != 0:
            item_list.append(page)
            offset = offset + 100
        else:
            break
    
    # merge all items from all searched pages        
    try:
        items_df = pd.concat(item_list,ignore_index=True).drop_duplicates().reset_index(drop=True)
    except:
        items_df = pd.DataFrame()

    # check which urls are new compared to old file
    try:    
        new_items = get_new_items(items_df, file_name, keyword)
    except:
        new_items = pd.DataFrame()
    
    items_df.to_csv(file_name) # save new response to csv
    return new_items

def send_message_per_item(df, chat_id='-425371692'):
    if len(df) > 0:
        for index, row in df.iterrows():
            message = """
            '{}' \n {}{} | {} KM | {} \n {}
            """.format(row['title'], unicodedata.lookup("EURO SIGN"),row['price'], row['distance'], row['city'], row['url'])
            print(message)
            telegram_send_text(bot_message=message, chat_id=chat_id)
    else:
        print("No items to message")
    return

def notify_concept2(chat_id='-425371692'):
    item_list = [
        check_new_items('concept 2', CategoryId='784'),
        check_new_items('concept 2 roeitrainer'),
        check_new_items('concept 2 roeimachine'),
        check_new_items('concept 2 roeiapparaat'),
        check_new_items('concept 2 ergometer'),
        check_new_items('concept 2 ergometer'),
        check_new_items('concept 2 roei'),
        check_new_items('concept 2 roeier'),
        check_new_items('concept 2 roeiertrainer'),
        check_new_items('concept 2 model'),
        check_new_items('concept 2 model b'),
        check_new_items('concept 2 model c'),
        check_new_items('concept 2 model d'),
        check_new_items('concept 2 model e'),
        check_new_items('concept II', CategoryId='784'),
        check_new_items('concept II roeitrainer'),
        check_new_items('concept II roeimachine'),
        check_new_items('concept II roeiapparaat'),
        check_new_items('concept II ergometer'),
        check_new_items('concept II ergometer'),
        check_new_items('concept II roei'),
        check_new_items('concept II roeier'),
        check_new_items('concept II roeiertrainer'),
        check_new_items('concept II model'),
        check_new_items('concept II model b'),
        check_new_items('concept II model c'),
        check_new_items('concept II model d'),
        check_new_items('concept II model e'),
        check_new_items('concept2', CategoryId='784'),
        check_new_items('concept2 roeitrainer'),
        check_new_items('concept2 roeimachine'),
        check_new_items('concept2 roeiapparaat'),
        check_new_items('concept2 ergometer'),
        check_new_items('concept2 ergometer'),
        check_new_items('concept2 roei'),
        check_new_items('concept2 roeier'),
        check_new_items('concept2 roeiertrainer'),
        check_new_items('concept2 model'),
        check_new_items('concept2 model b'),
        check_new_items('concept2 model c'),
        check_new_items('concept2 model d'),
        check_new_items('concept2 model e'),
        check_new_items('conceptII', CategoryId='784'),
        check_new_items('conceptII roeitrainer'),
        check_new_items('conceptII roeimachine'),
        check_new_items('conceptII roeiapparaat'),
        check_new_items('conceptII ergometer'),
        check_new_items('conceptII ergometer'),
        check_new_items('conceptII roei'),
        check_new_items('conceptII roeier'),
        check_new_items('conceptII roeiertrainer'),
        check_new_items('conceptII model'),
        check_new_items('conceptII model b'),
        check_new_items('conceptII model c'),
        check_new_items('conceptII model d'),
        check_new_items('conceptII model e')
    ]
    new_items = pd.concat(item_list,ignore_index=True).drop_duplicates().reset_index(drop=True)
    send_message_per_item(df=new_items, chat_id=chat_id)
    return

def notify_sansui(chat_id='-482088244'):
    item_list = [
        check_new_items('sansui', CategoryId=31),
        check_new_items('sansui au 5500 ', CategoryId=31)
    ]
    new_items = pd.concat(item_list,ignore_index=True).drop_duplicates().reset_index(drop=True)
    send_message_per_item(df=new_items, chat_id=chat_id)
    return

def notify_synths(chat_id='-425619351'):
    item_list = [
        check_new_items('korg polysix', CategoryId=31),
        check_new_items('poly-61', CategoryId=31),
        check_new_items('poly 61', CategoryId=31),
        check_new_items('korg ms-20', CategoryId=31),
        check_new_items('korg ms 20', CategoryId=31),
        check_new_items('korg ms20', CategoryId=31),
        check_new_items('moog grandmother', CategoryId=31),
        check_new_items('moog matriarch', CategoryId=31),
        check_new_items('moog sub 37', CategoryId=31),
        check_new_items('moog subsequent 37', CategoryId=31),
        check_new_items('moog sub phatty', CategoryId=31),
        check_new_items('moog voyager', CategoryId=31),
        check_new_items('oberheim matrix 1000', CategoryId=31),
        check_new_items('oberheim m1000', CategoryId=31),
        check_new_items('oberheim m 1000', CategoryId=31),
        check_new_items('oberheim matrix 6r', CategoryId=31),
        check_new_items('oberheim ob-6', CategoryId=31),
        check_new_items('oberheim ob6', CategoryId=31),
        check_new_items('oberheim ob 6', CategoryId=31),
        check_new_items('dave smith prophet 5', CategoryId=31),
        check_new_items('dave smith prophet 6', CategoryId=31),
        check_new_items('dave smith prophet 8', CategoryId=31),
        check_new_items('roland j3-xp', CategoryId=31),
        check_new_items('roland juno 106', CategoryId=31),
        check_new_items('roland juno 6', CategoryId=31),
        check_new_items('roland juno 60', CategoryId=31)
    ]
    new_items = pd.concat(item_list,ignore_index=True).drop_duplicates().reset_index(drop=True)
    send_message_per_item(df=new_items, chat_id=chat_id)
    return