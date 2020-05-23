import urllib.request
import json
import pandas as pd

# url, hoogste bod, vraagprijs
url = 'https://www.marktplaats.nl/lrp/api/search?limit=30&offset=0&postcode=2012EG&query=concept%202&searchInTitleAndDescription=true&sortBy=SORT_INDEX&sortOrder=DECREASING&viewOptions=list-view'

# https://www.marktplaats.nl/vip-similar-listings.json?categoryId=748&sellerId=3654851&itemId=m1548092296&_=1589617403060

def get_response(query_url):
    # get response
    response = urllib.request.urlopen(query_url)
    jresponse = json.load(response)

    # save to json
    with open('data.json', 'w') as fp:
        json.dump(jresponse, fp, sort_keys=True, indent=4)
    return jresponse

df = get_response(url)