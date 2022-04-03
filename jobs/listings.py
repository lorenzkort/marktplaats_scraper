import logging
from jobs.api import get
import pandas as pd
from jobs.config.core import DATASET_DIR, config
import re
import unicodedata

base_url = 'https://www.marktplaats.nl'

# generate url based on keyword, category ID, and Title and Description
def url_gen(keyword='', categoryId='', titleAndDescription=False, postalcode='2012EG'):
    if keyword != '':
        keyword = str(keyword).replace(' ', '%20')
    if categoryId != '':
        categoryId = 'l1categoryId=' + str(categoryId)
    if titleAndDescription == True:
        titleAndDescription = '&searchIntitleAndDescription=true'
    else:
        titleAndDescription = ''
    url = f'https://www.marktplaats.nl/lrp/api/search?{categoryId}&limit=100&offset=0&postcode={postalcode}&query={keyword}{titleAndDescription}&sortBy=SORT_INDEX&sortOrder=DECREASING'
    return url

def c2type(title):
    if re.search(' b( |$)', title, flags=re.IGNORECASE):
        return 'B'
    if re.search(' c( |$)', title, flags=re.IGNORECASE):
        return 'C'
    if re.search(' d( |$)', title, flags=re.IGNORECASE):
        return 'D'
    if re.search(' e( |$)', title, flags=re.IGNORECASE):
        return 'E'
    return None

def monitortype(title):
    if re.search('pm2( |$)', title, flags=re.IGNORECASE):
        return 'PM2'
    if re.search('pm3( |$)', title, flags=re.IGNORECASE):
        return 'PM3'
    if re.search('pm4( |$)', title, flags=re.IGNORECASE):
        return 'PM4'
    if re.search('pm5( |$)', title, flags=re.IGNORECASE):
        return 'PM5'
    return None

def target_price(c2type, monitortype):
    if c2type == None or monitortype == None:
        return 0
    c2price = {
        'B': 200,
        'C': 400,
        'D': 600,
        'E': 650
    }
    monitorprice = {
        'PM2': 50,
        'PM3': 100,
        'PM4': 100,
        'PM5': 200,
    }
    return c2price[c2type] + monitorprice[monitortype]
    

def clean_items(items):
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
                price = int(price / 100)
            else:
                price = 'NaN'
        except Exception as e:
            logging.info(e)
            price = 'NaN'
        try:
            distance = float(item['location']['distanceMeters'])
            if distance > 0:
                distance = int(distance / 1000)
            else:
                distance = '0'
        except:
            distance = '0'

        title = item['title'].replace('&','').replace("'", "").replace('"', '').replace(config.csv_delimiter, '')
        t_price = target_price(c2type(title), monitortype(title))
        if type(price) == int and t_price != 0:
            margin = t_price - price
            if margin < 0:
                margin = 0
        else:
            margin = 0
        
        items[index] = {
            'id': item['itemId'],
            'title': title,
            'url': base_url + item['vipUrl'],
            'price': price,
            'sellerId': str(item['sellerInformation']['sellerId']),
            'advertType': advertType,
            'distance': distance,
            'city': item['location']['cityName'],
            'c2type': c2type(title),
            'monitortype': monitortype(title),
            'target_price': t_price,
            'margin': margin,
            'date':item['date']
        }
    return items

def filter_seller_id(df, sellerIds, keyword):
    if len(df) > 0: # check if dataframe is not empty
        logging.info(f'{keyword}: {len(df)} items in API response')
        df = df[df['advertType']== 'PACKAGE_FREE']
        for id in sellerIds:
            df = df[df['sellerId']!=str(id)] #filter out sellers by their marktplaats ID
        if len(df) == 0:
            logging.info(f"{keyword}: {len(df)} items left after filtering")
    else:
        logging.info(f"{keyword}: {len(df)} items in API response")
    return df

def get_listings(keyword, categoryId, titleAndDescription=False, postalcode=config.postalcode,spam_sellers=[]):
    # create url
    query_url = url_gen(keyword=keyword, categoryId=categoryId, titleAndDescription=titleAndDescription, postalcode=postalcode)

    # get listings from Marktplaats API
    response = get(query_url)
    items = response.json()["listings"]   
    items = clean_items(items)

    # filter dataframe based on advertisement type and user ID
    df = filter_seller_id(pd.DataFrame(items), spam_sellers, keyword)
    
    return df

if __name__ == "__main__":
    keyword = 'concept 2'
    categoryId = '784'
    spam_sellers = [25776758]
    df = get_listings(keyword, categoryId, titleAndDescription=False, postalcode='2012EG', spam_sellers=spam_sellers)
    save = df.to_csv(DATASET_DIR / 'listings.csv')