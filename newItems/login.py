import requests
from bs4 import BeautifulSoup as bs

headers = {
    'user-agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36',
    'referer': 'https://www.marktplaats.nl/account/login.html?target=https%3A%2F%2Fwww.marktplaats.nl%2F'
    }

payload = {
    'email':'mickvanmierlo@outlook.com',
    'password':'roeitrainer2000',
    'rememberMe':'true',
    'successUrl':'https://www.marktplaats.nl/'
}

def save_html(html,f_name):
    f = open(f_name, 'w+')
    f.write(str(bs(html, 'lxml').prettify()))
    return

with requests.Session() as s:
    url = 'https://www.marktplaats.nl/account/login'
    r = s.get(url, headers=headers)
    save_html(r.content,'out1.html')
    s.post(url, data=payload, headers=headers)
    save_html(r.content,'out2.html')

# check file differences
with open('out1.html', 'r') as o1, open('out2.html', 'r') as o2:
    if o1 == o2:
        print('same files')
    else:
        print('different files')

