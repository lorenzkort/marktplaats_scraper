"""
Purpose of a Channel is to:
- Execute every minute:
    - Aggregate all unique listings connected to the channel
    - Check if there are listing-ID's unkown to the saved csv
    - If an listing-ID is not yet in the saved Dataframe
        - Send a message on Telegram with:
            - Title
            - Price
            - Distance from postalcode
            - Expected margin
            - Link
        - Add new listing with all info to csv
"""
import logging
from jobs import telegram
from jobs.config.core import config, DATASET_DIR
from jobs.listings import get_listings, target_price
import pandas as pd
import unicodedata

def get_saved_listing_ids(chatId) -> set:
    """
    Gets a dataframe of all unique listing-IDs known to the application for the channel
    """
    filename = str(chatId).replace('-','')
    try:
        df = pd.read_csv(f'{DATASET_DIR}/channels/{filename}.csv', delimiter='|')
    except pd.errors.EmptyDataError:
        logging.info(f"{chatId}: No known id's")
        return set()
    known_ids = set(df['id'])
    
    return known_ids

def aggregate_called_listings(chatId) -> pd.DataFrame:
    """
    - Aggregates all unique listings connected to the channel
    - Removes all listings having a known listing-ID
    - Returns dataframe with new items
    """
    searches = [x.searches for x in config.channels if x.chatId == chatId][0]
    channel = [x for x in config.channels if x.chatId == chatId][0]
    set_of_searches = []

    for s in searches:
        search = get_listings(
            keyword=s.keyword, 
            categoryId=s.categoryId,
            titleAndDescription=s.titleAndDescription,
            postalcode=channel.postalcode, 
            spam_sellers=channel.spam_sellers)
        set_of_searches.append(search)
    
    unique_listings = pd.concat(set_of_searches)
    unique_listings.drop_duplicates(subset="id")

    return unique_listings

def get_new_listings(chatId, saved_ids) -> pd.DataFrame:
    """
    Creates dataframe of listings having an unkown listing-ID
    """
    called_listings = aggregate_called_listings(chatId)
    new_listings = called_listings[~called_listings['id'].isin(saved_ids)]
    new_listings.set_index("id", inplace = True)
    
    return new_listings

def save_new_listings(chatId, new_listings: pd.DataFrame) -> None:
    """
    Appends new listings to channel CSV
    """
    filename = str(chatId).replace('-','') + '.csv'
    filepath = f'{DATASET_DIR}/channels/{filename}'

    if len(new_listings) == 0:
        return
    if len(open(filepath, 'r').readlines()) > 1:
        header = False
    else:
        header = True

    new_listings.to_csv(f'{DATASET_DIR}/channels/{filename}', mode='a', sep='|', header=header)

    return

def send_messages(chatId, new_listings: pd.DataFrame) -> None:
    """
    Goes through listings and sends a formatted message in the chat with:
            - Title
            - Price
            - Distance from postalcode
            - Expected margin
            - Average sales price
            - Link
    """
    for listing in new_listings.itertuples():
        if listing.margin > 0:
            margin = f'\nExpected margin: €{listing.margin}'
        else:
            margin = ''
        if listing.target_price > 0:
            target_price = f'\nAverage sales price: €{listing.target_price}'
        else:
            target_price = ''
        message = f"""
            '{listing.title}' \n {unicodedata.lookup("EURO SIGN")}{listing.price} | {listing.distance} KM | {listing.city}{target_price}{margin}\n{listing.url}
            """
        telegram.send_text(msg=message, chatId=chatId)
    return

def check_for_new_listings(chatId) -> None:
    saved_ids = get_saved_listing_ids(chatId)
    new_listings = get_new_listings(chatId, saved_ids)
    save_new_listings(chatId, new_listings)
    # send_messages(chatId, new_listings)
    return

if __name__ == "__main__":
    chatId = -1001797708509
    saved_ids = get_saved_listing_ids(chatId)
    new_listings = get_new_listings(chatId, saved_ids)
    save_new_listings(chatId, new_listings)
    send_messages(chatId, new_listings)
    print(new_listings)