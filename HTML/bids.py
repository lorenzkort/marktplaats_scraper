'''
    for bid in item_bids:
        bid_person = bid.find('span', {'class': 'vip-bid-bidder-name-default-view bid-name ellipsis'}).text
        bid_price = bid.find('span', {'class': 'vip-bid-amount-default-view bid-amount'}).text
        bid_date = bid.find('span', {'class': 'vip-bid-date-default-view bid-date'}).text
        bids.append({
                'bid_person': bid_person,
                'bid_price': bid_price,
                'bid_date': bid_date
            })
    item = {
        'bids': bids,
    }
    print(len(item['bids']))
    '''