from selector import Selector
from npr import NPRParser
from infowars import InfowarsParser

######
# url = 'https://www.npr.org/sections/politics/'
# url = 'https://www.infowars.com/news/'

s = Selector(
    NPRParser('https://www.npr.org/'),
    InfowarsParser('https://www.infowars.com/', rude=True),
)

prs = s.match(url)
content = s.scrape(prs, url)
from pprint import pprint
pprint(content)
