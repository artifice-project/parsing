from selector import NPRParser

######

npr = NPRParser('http://www.npr.org')
url = 'http://www.npr.org/sections/politics'
print('URL: {}'.format(url))
yn = npr.is_allowed(url)
print('Allowed? {}'.format(yn))
response = npr.get_request(url)
d = npr.extract_content(response)
from pprint import pprint
pprint(d)
