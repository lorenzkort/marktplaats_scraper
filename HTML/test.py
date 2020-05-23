from requests_html import HTMLSession
from bs4 import BeautifulSoup

url = 'https://www.marktplaats.nl/l/caravans-en-kamperen/campers/#q:volkswagen+t3|PriceCentsFrom:100000|PriceCentsTo:700000|constructionYearTo:2001|sortBy:SORT_INDEX|sortOrder:DECREASING|postcode:2012EG'
session = HTMLSession()
r = session.get(url)
r = r.html.html
soup = BeautifulSoup(r)
print(soup)

with open("advertentie.html", "w+") as file:
        file.write(soup.prettify())