from selector import Selector
from npr import NPRParser

######
url = 'https://www.npr.org/sections/politics'

s = Selector(
    NPRParser('https://www.npr.org/'),
)

prs = s.match(url)
content = s.scrape(prs, url)
from pprint import pprint
pprint(content)


# npr = NPRParser('https://www.npr.org/')
# url = 'http://www.npr.org/sections/politics'
# print('URL: {}'.format(url))
# yn = npr.is_allowed(url)
# print('Allowed? {}'.format(yn))
# response = npr.get_request(url)
# d = npr.extract_content(response)
# from pprint import pprint
# # pprint(d)
