# libaries for getting data
from bs4 import BeautifulSoup
import requests
import datetime

# libraries for parsing data
import pandas as pd

def get_soup(url):
    page = requests.get(url).text
    soup = BeautifulSoup(str(page), 'html.parser')
    return soup

def get_item_urls(search_soup):
    user_listings = search_soup.find('ul', class_ = 'mp-Listings mp-Listings--list-view')
    items = user_listings.find_all('li', class_ = 'mp-Listing mp-Listing--list-item')
    item_url_list = []
    for item in items:
        item_url = item.find('a', class_ = 'mp-Listing-coverLink', href=True)['href']
        item_url_list.append('https://www.marktplaats.nl' + item_url)
    return item_url_list

#item_soup = get_soup('https://www.marktplaats.nl/a/sport-en-fitness/roeien/m1545651210-concept-2-roeitrainer-pm2-display.html') # test url

 #with open("output1.html", "w+") as file:
  #  file.write(str(item_soup.prettify()))

def parse_item(url):
    item = get_soup(url)
    try:
        bids = int(len(item.find_all('li', class_ = 'bid mp-Card-block')))
    except:
        bids = 9999999
    try:
        views = int(item.find('span', {'id': 'view-count'}).text)
    except:
        views = 9999999
    try:
        likes = int(item.find('span', {'id': 'favorited-count'}).text.strip())
    except:
        likes = 9999999
    item = {
        '1_url': url,
        '2_bids': bids,
        '3_views': views,
        '4_likes': likes
    }
    return item

if __name__ == "__main__":
    index = 1
    df = pd.DataFrame()
    while True:
        search_url = 'https://www.marktplaats.nl/l/sport-en-fitness/f/zo-goed-als-nieuw/31/p/' + str(index) + '#offeredSince:Een%20week|f:32|sortBy:SORT_INDEX|sortOrder:DECREASING'
        search_soup = get_soup(search_url) # get html from search
        item_urls = get_item_urls(search_soup) # get item urls from html
        if len(item_urls) < 5:
            break
        item_list = []
        for item_index, url in enumerate(item_urls): # get data from items
            item = parse_item(url)
            print('p' + str(index) + 'i' + str(item_index + 1))
            df = df.append(item, ignore_index=True)
        if (index % 50) == 0:
            df = df.drop_duplicates()
            df = df.astype({'2_bids': int, '3_views': int, '4_likes': int})
            df = df.sort_values('3_views', ascending=False)
            today = str(datetime.date.today()).replace('-','') # defines today's date
            csv_name = today + '_mp_' + str(index) + '.csv'
            df.to_csv(csv_name)
            df = pd.DataFrame()
        index = index + 1