# parsing

Independent module for development, testing, and benchmarking of webpage scraper classes. `BaseParser` is an abstract class to be inherited by all other parsers, as it contains all of the required functionality to parse a site and extract its content. Parsers are automatically compliant to directives located in the `robots.txt` file at a website's root--if no file is found, the parser will raise an error unless the param `ignore-missing-directive` override is set to True.

## Creating an inherited class
There are only 4 methods that are not implemented in the Base class, for obvious reason. These are:
```python
cls.parse_title()
cls.parse_text()
cls.parse_captions()
cls.parse_links()
```
These methods all take in a BeautifulSoup object and from it, extract the relevant data. Each site you wish to scrape will be somewhat different, and these abstract methods allow for custom extraction while still maintaining access to the robust functionality of the Base class.

## Boilerplate
```python
from base import BaseParser

class MyParser(BaseParser):
  '''
  Docstring for MyParser class
  '''
  def __init__(self, url_root):
    super().__init__(url_root)

  def parse_title(self, soup):
    # logic goes here
    pass

  def parse_text(self, soup):
    # logic goes here
    pass

  def parse_captions(self, soup):
    # logic goes here
    pass

  def parse_links(self, soup):
    # logic goes here
    pass
```

## Usage
A simple invocation procedure is as follows. Note that the object should only be instantiated once, as all of the functionality used in extracting the content is done through static and class methods.
```python
from custom import MyParser

parser = MyParser('https://www.example.com/')

url_to_scrape = 'https://www.example.com/story/42?timezone=eastern'
allowed = parser.is_allowed(url_to_scrape)
if allowed:
  response = parser.get_request(url_to_scrape)
  data = parser.extract_content(response)
```
