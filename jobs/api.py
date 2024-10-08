import logging
import requests
import time
from jobs.telegram import send_text
from jobs.config.core import DATASET_DIR

def get(query_url):
    try:
        headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36',
        'referer': 'https://www.marktplaats.nl/q/concept+2/',
        'pragma': 'no-cache',
    }
        cookies = {"rbzid":"4xlWoDPOu+MgLjLMjkxVS3yyCIO2gtLWSaUXHVqU553tdMx4FWtm8OdONYZbzxorD/lcx84qCyxkKyBSWDY+gKi4YdtnFvnP/AIgjIW11tFyEFxexMgdvsmQ5da1fyVWiYva8Yf+DjFvUOfbZQ7iuFJkMKxkEiiZrj7EwjCz262C1ax531w7rf9YqsKaLSQIRZ2oEOA+jKKJp4Qc7w7YdY1iKIs4wBv8iAcn+3z1W6oij7QlPFejj8aJxsMH0/EUr+MjuJbsbYgFOV4mZC+XRTG+L+6twxqvZ6Tjp9bs1qe2VUzjqvO4TL/xN24Ov1we"}
        response = requests.get(query_url, headers=headers, cookies=cookies)
    except:
        logging.info(f'API error: {response} on URL: {query_url}')
    time.sleep(0.01)
    return response

if __name__ == "__main__":
    r = get('https://www.marktplaats.nl/lrp/api/search?l1CategoryId=784&limit=100&offset=0&postcode=2012EG&query=concept%202&sortBy=SORT_INDEX&sortOrder=DECREASING')
    listings = r.json()['listings']
    with open(DATASET_DIR / 'API/response.json', 'w+') as f:
        [f.write(str(x).replace("'",'"') + '\n') for x in listings]
    for item in listings:
        row = f"{item['date']} - {item['title']}"
        print(row)