from request_item import check

if __name__ == "__main__":
    check('Concept 2',  'https://www.marktplaats.nl/lrp/api/search?l1CategoryId=784&limit=100&offset=0&postcode=2012EG&query=concept%202&searchInTitleAndDescription=true&sortBy=SORT_INDEX&sortOrder=DECREASING&viewOptions=list-view', '-425371692')
    check('Concept2',  'https://www.marktplaats.nl/lrp/api/search?l1CategoryId=784&limit=100&offset=0&postcode=2012EG&query=concept%202&searchInTitleAndDescription=true&sortBy=SORT_INDEX&sortOrder=DECREASING&viewOptions=list-view', '-425371692')
    check('Marzocco',   'https://www.marktplaats.nl/lrp/api/search?limit=100&offset=0&postcode=2012EG&query=marzocco&sortBy=SORT_INDEX&sortOrder=DECREASING&viewOptions=list-view', '-367307171')
    check('Anfim',      'https://www.marktplaats.nl/lrp/api/search?limit=100&offset=0&postcode=2012EG&query=anfim&sortBy=SORT_INDEX&sortOrder=DECREASING&viewOptions=list-view', '-367307171')
    check('Mahlkonig',  'https://www.marktplaats.nl/lrp/api/search?limit=100&offset=0&postcode=2012EG&query=mahlkonig&sortBy=SORT_INDEX&sortOrder=DECREASING&viewOptions=list-view', '-367307171')
    check('Mazzer',     'https://www.marktplaats.nl/lrp/api/search?limit=100&offset=0&postcode=2012EG&query=mazzer&sortBy=SORT_INDEX&sortOrder=DECREASING&viewOptions=list-view', '-367307171')
    check('Fiorenzato', 'https://www.marktplaats.nl/lrp/api/search?limit=100&offset=0&postcode=2012EG&query=fiorenzato&sortBy=SORT_INDEX&sortOrder=DECREASING&viewOptions=list-view', '-367307171')
    check('roeitrainer', 'https://www.marktplaats.nl/lrp/api/search?attributesById[]=32&attributesById[]=31&limit=30&offset=0&postcode=2012EG&query=roeitrainer&sortBy=SORT_INDEX&sortOrder=DECREASING&viewOptions=list-view', '-382732462')
    check('roei trainer', 'https://www.marktplaats.nl/lrp/api/search?attributesById[]=32&attributesById[]=31&limit=30&offset=0&postcode=2012EG&query=roei%20trainer&sortBy=SORT_INDEX&sortOrder=DECREASING&viewOptions=list-view', '-382732462')
    check('roeiapparaat', 'https://www.marktplaats.nl/lrp/api/search?attributesById[]=32&attributesById[]=31&limit=30&offset=0&postcode=2012EG&query=roeiapparaat&sortBy=SORT_INDEX&sortOrder=DECREASING&viewOptions=list-view', '-382732462')
    check('roei apparaat', 'https://www.marktplaats.nl/lrp/api/search?attributesById[]=32&attributesById[]=31&limit=30&offset=0&postcode=2012EG&query=roei%20apparaat&sortBy=SORT_INDEX&sortOrder=DECREASING&viewOptions=list-view', '-382732462')
    check('roeier', 'https://www.marktplaats.nl/lrp/api/search?attributesById[]=32&attributesById[]=31&limit=30&offset=0&postcode=2012EG&query=roeier&sortBy=SORT_INDEX&sortOrder=DECREASING&viewOptions=list-view', '-382732462')
    check('roeimachine', 'https://www.marktplaats.nl/lrp/api/search?attributesById[]=32&attributesById[]=31&limit=30&offset=0&postcode=2012EG&query=roeimachine&sortBy=SORT_INDEX&sortOrder=DECREASING&viewOptions=list-view', '-382732462')
    check('roei machine', 'https://www.marktplaats.nl/lrp/api/search?attributesById[]=32&attributesById[]=31&limit=30&offset=0&postcode=2012EG&query=roei%20machine&sortBy=SORT_INDEX&sortOrder=DECREASING&viewOptions=list-view', '-382732462')
    check('roeibank', 'https://www.marktplaats.nl/lrp/api/search?attributesById[]=32&attributesById[]=31&limit=30&offset=0&postcode=2012EG&query=roeibank&sortBy=SORT_INDEX&sortOrder=DECREASING&viewOptions=list-view', '-382732462')
    check('roei bank', 'https://www.marktplaats.nl/lrp/api/search?attributesById[]=32&attributesById[]=31&limit=30&offset=0&postcode=2012EG&query=roei%20bank&sortBy=SORT_INDEX&sortOrder=DECREASING&viewOptions=list-view', '-382732462')
