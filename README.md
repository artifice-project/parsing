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

---
## Documentation

`BaseParser(url_root, user_agent='*', upgrade_insecure=True, use_defaults=True, ignore_missing_directive=False)`

Constructor for the parser base class, inherited by all child classes.

`url_root` is the 'homepage' of the website, and should be specified with the complete scheme proceeding the address (http[s]://). Extraneous path data will be disregarded from the url. In the case that the url_root is not a valid URL, an error will be raised. The url_root is used both to strain links that are gathered from a page by disregarding links that do not have the same netloc, as well as to create the typical robots.txt path.

`user_agent` is the identifier to be used when sending requests. By convention, the user agent should include a human-readable name by which to refer to the bot as, and should additionally include either as associated website or contact email such that the webmaster of the target site may contact in the event of an issue. This is not a legal requirement; however, it is very highly encouraged and is to be expected of any respectable developer.

`upgrade_insecure` is whether or not to default to using HTTPS when sending requests to target sites. In some cases, such as where the target site is not using a valid certificate, this may be best left disabled, but in most cases should be left as the default value of True.

`use_defaults` controls how empty fields are handled when extracting content. In the case that an attribute is not present, the field may be assigned to be the empty default. A string field would be set as `''`, a list `[]`, etc. This parameter should be left to true unless robust, custom schema validation is being used elsewhere in the pipeline.

`ignore_missing_directive` controls whether or not to raise an error in the case that a valid robots.txt file is not found at the expected location. Should no file exist, all URLs will be considered allowable. This can lead to undesirable behavior for both the developer and the target site owner, as resources such as JavaScript files, authenticated domains, and extraneous paths will be considered relevant. If you are determined to scrape without a robots.txt file, be sure to perform plenty of testing ahead of deployment to identify and correct for any abnormal behavior.

---
`BaseParser.is_url(url)`

Static method, returns a boolean value indicative of whether or not the argument is a valid URL. Relative URLs, URLs without a protocol schema, and anchor links will all return False.

---
`BaseParser.netloc(url)`

Static method, returns the netloc of argument url. Netloc is the "human-friendly" URL, and does not include the protocol schema or appended path. An example netloc is `www.google.com`

---
`BaseParser.remove_duplicates(lst)`

Static method, used to remove repeated elements from a list. Non-mutative, such that it is safe for use on critical objects not intended to be mutable. Will raise error if called on objects other than lists.

---
`BaseParser.pour_soup(response)`

Static method, used to create a BeautifulSoup object from request response content. Defaults to using the html.parser protocol.

---
`BaseParser.same_site(link)`

Checks whether or not the link points to an internal or external location. References the url_root attribute of the object and compares the netloc of both that and the argument link. Returns a boolean value.

---
`BaseParser.is_allowed(url)`

Checks the robots.txt directives to determine if the provided URL is allowable for scraping. Returns a boolean value.

---
`BaseParser.get_request(url)`

Convenience function to execute requests.get, with the addition of the specified User-Agent in the request header. Returns a requests response object no matter what, expect in the case of an IOError or ConnectionError. Is is useful to check the returned value to ensure that value.status_code == 200 before proceeding.

---
`BaseParser.parse_title`

Abstract method, NotImplementedError raised unless logic is supplied in inherited class. Expected return type is a string.

---
`BaseParser.parse_text`

Abstract method, NotImplementedError raised unless logic is supplied in inherited class. Expected return type is a string.

---
`BaseParser.parse_captions`

Abstract method, NotImplementedError raised unless logic is supplied in inherited class. Expected return type is a list.

---
`BaseParser.parse_links`

Abstract method, NotImplementedError raised unless logic is supplied in inherited class. Expected return type is a list.

---
`BaseParser.strain_links(links)`

Filters and removed any duplicate items contained in the extracted list of URLs. Additionally, any URLs which do not return a True value from the function `is_url()` are omitted.

---
`BaseParser.extract_content(response)`

Main entry point for parsing request content data. Returns a dictionary object with attributes `text`, `title`, `captions`, and `links`.
