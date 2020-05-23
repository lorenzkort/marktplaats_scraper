from request_item import check

if __name__ == "__main__":
    check('Concept 2', 'https://www.marktplaats.nl/lrp/api/search?limit=30&offset=0&postcode=2012EG&query=concept%202&searchInTitleAndDescription=true&sortBy=SORT_INDEX&sortOrder=DECREASING&viewOptions=list-view')
    check('Marzocco', 'https://www.marktplaats.nl/lrp/api/search?limit=30&offset=0&postcode=2012EG&query=marzocco&searchInTitleAndDescription=true&sortBy=SORT_INDEX&sortOrder=DECREASING&viewOptions=list-view')