import urllib.request
import requests
import json
import pandas as pd
from bs4 import BeautifulSoup

def get_soup(url):
    page = requests.get(url).text
    soup = BeautifulSoup(str(page), 'html.parser')
    return soup

def get_max_bid(item_url):
    soup = get_soup(item_url)
    bids_soup = soup.find_all('li', class_ = 'bid mp-Card-block')
    bids = []
    for bid in bids_soup:
        bid_person = bid.find('span', {'class': 'vip-bid-bidder-name-default-view bid-name ellipsis'}).text
        try:
            bid_price = int(bid.find('span', {'class': 'vip-bid-amount-default-view bid-amount'}).text.replace('€','').replace('.', '').replace(',','').strip())
        except:
            bid_price = 0
        bid_date = bid.find('span', {'class': 'vip-bid-date-default-view bid-date'}).text
        bids.append({
                'bid_person': bid_person,
                'bid_price': bid_price,
                'bid_date': bid_date
            })
    if bids != []:
        max_bid = max([i['bid_price'] for i in bids]) / 100
    else:
        max_bid = None
    return max_bid

def get_items(query_url, page_nr):
    # get query url
    offset = (page_nr * 100) - 100
    query_url = query_url.replace('offset=0', 'offset=' + str(offset)).replace('limit=30', 'limit=100')

    # get response
    response = urllib.request.urlopen(query_url)
    jresponse = json.load(response)

    # get items
    items = jresponse["listings"]
    base_url = 'https://www.marktplaats.nl'
    for index, item in enumerate(items):
        url = base_url + item['vipUrl']
        itemType = item['priceInfo']['priceType']
        askPrice = item['priceInfo']['priceCents'] / 100
        maxBid = get_max_bid(url)
        try: 
            bidAskDiff = maxBid - askPrice
        except:
            bidAskDiff = None
        priorityProduct = item['priorityProduct']
        distanceMeters = item['location']['distanceMeters']
        date = item['date']

        items[index] = {
            'url': url,
            'type': itemType,
            'askPrice': askPrice,
            'maxBid': maxBid,
            'bidAskDiff': bidAskDiff,
            'priorityProduct': priorityProduct,
            'distanceMeters': distanceMeters,
            'date': date
        }
    df = pd.DataFrame(items)
    return df

def filter_items(df):
    df = df[df['askPrice'] > 0]
    df = df[df['maxBid'] > 0]
    return df

def get_pages(url):
    page = 1
    total_items = pd.DataFrame()
    while True:
        # get filtered items from page
        print('page ', page)
        items = get_items(url, page)
        items = filter_items(items)

        # if page has less than 2 items, stop
        if len(items) < 2:
            break
        
        # append items to dataframe
        total_items = total_items.append(items, ignore_index=True)
        
        # fill each csv with at least x items
        if total_items.shape[0] > 10000:
            total_items.to_csv('items_' + str(page) + '.csv')
            total_items = pd.DataFrame()
            print('saved')

        page = page + 1 # increase page-id
    return

url = '&postcode=2012EG&query=concept%202&sortBy=SORT_INDEX&sortOrder=DECREASING&viewOptions=list-view'
url_2 = 'https://www.marktplaats.nl/lrp/api/search?attributesById[]=32&attributesById[]=31&l1CategoryId=728&limit=30&offset=0&postcode=2012EG&sortBy=SORT_INDEX&sortOrder=INCREASING&viewOptions=list-view'
get_pages(url_2)