import requests

url = 'https://api.marktplaats.nl/v1/advertisements/m1545428672/bids'

url2= 'https://api.marktplaats.nl/v1/advertisements/m1545428672/bids/get'

url3 = 'https://www.marktplaats.nl/lrp/api/v1/advertisements/m1545428672/bids/'
response = requests.get(url2)
print(response)