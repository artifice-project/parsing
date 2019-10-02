import os
import requests
import urllib, urllib.robotparser
from abc import ABC, abstractmethod


class BaseParser(ABC):
    '''
    Parent of all parser classes. Parser should be instantiated once,
    and used repeatedly to parse and extract content. Upon creation,
    the object will seek out the `robots.txt` file and store the
    directives contained within it. In the case that a URL is provided
    that is not allowed by the directives, the called method will return
    a <None> type object. Otherwise, the method will return a dictionary
    containing the expected fields. Any field that was not successfully
    parsed or that does not return a value can be either rendered as the
    default type for that attribute, or as a <None> type field.
    '''
    @staticmethod
    def is_url(url):
        try:
            result = urllib.parse.urlparse(url)
            return all([result.scheme, result.netloc])
        except ValueError:
            return False


    @staticmethod
    def netloc(url):
        return urllib.parse.urlparse(url).netloc


    def same_site(self, link):
        # checks whether the link points to an internal location
        nl_1 = self.netloc(self.url_root)
        nl_2 = self.netloc(link)
        return True if nl_1 == nl_2 else False


    def __init__(self, url_root, user_agent='*',  upgrade_insecure=False, use_defaults=True):
        '''
        param:  url_root         <str>      URL netloc
        param:  upgrade_insecure <bool>     http --> https
        param:  use_defaults     <bool>     return empty instance of type,
         rather than none in the case that data is not present.

        return: content          <dict>
        '''
        self.user_agent = user_agent
        self.use_defaults = use_defaults
        self.upgrade_insecure = upgrade_insecure

        if not self.is_url(url_root):
            raise ValueError('{0} must be a valid url'.format(url_root))

        url = urllib.parse.urlparse(url_root)

        self.url_root = url.scheme + '://' + url.netloc
        self.robots_url = os.path.join(self.url_root, 'robots.txt')

        self.rp = urllib.robotparser.RobotFileParser()
        self.rp.set_url(self.robots_url)
        self.rp.read()


    def is_allowed(self, url):
        '''
        Checks robots.txt parser to see if url is allowed.
        '''
        generic_user_agent = '*'
        return self.rp.can_fetch(generic_user_agent, url)


    @staticmethod
    def remove_duplicates(lst):
        return list(dict.fromkeys(lst))


    @staticmethod
    def pour_soup(response):
        from bs4 import BeautifulSoup
        html = response.content
        parser = 'html.parser'
        soup = BeautifulSoup(html, parser)
        return soup


    @abstractmethod
    def parse_title(self, soup):
        '''
        Takes in a <BS4 Soup> object, extracts data.
        '''
        raise NotImplementedError


    @abstractmethod
    def parse_captions(self, soup):
        '''
        Takes in a <BS4 Soup> object, extracts data.
        '''
        raise NotImplementedError


    @abstractmethod
    def parse_text(self, soup):
        '''
        Takes in a <BS4 Soup> object, extracts data.
        '''
        raise NotImplementedError


    @abstractmethod
    def parse_links(self, soup):
        '''
        Takes in a <BS4 Soup> object, extracts data.
        '''
        raise NotImplementedError


    def strain_links(self, links):
        '''
        Filters and removes any links that are not worth scraping,
        these could be anchor tags within the same page or ones
        that would cause the scraper to leave the site.
        '''
        strained = []
        for link in links:
            if self.is_url(link) and self.same_site(link):
                strained.append(link)
        return strained


    def extract_content(self, response):
        '''
        params: response <Response>
        returns: content <dict>
        '''
        soup = self.pour_soup(response)

        _title =     self.parse_title(soup)
        _captions =  self.parse_captions(soup)
        _text =      self.parse_text(soup)
        _links =     self.parse_links(soup)

        return dict(
            origin=response.url,
            title=_title,
            text=_text,
            captions=_captions,
            links=_links,
        )


    def get_request(self, url):
        if self.upgrade_insecure and urlparse(url).schema == 'http':
            url = url.replace('http', 'https')
        headers = {'User-Agent': self.user_agent}
        response = requests.get(url, headers=headers)
        return response

    # # @allowed ((class method decorator))
    # def allowed(foo):
    #     def magic(self) :
    #         print("start magic")
    #         foo(self)
    #         print(self.url_root)
    #         print("end magic")
    #     return magic
