import os
import requests
import urllib, urllib.parse, urllib.robotparser
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
    def __init__(self,
                url_root,
                user_agent='*',
                upgrade_insecure=True,
                use_defaults=True,
                ignore_missing_directive=False):
        '''
        param:  url_root         <str>      URL netloc
        param:  upgrade_insecure <bool>     http --> https
        param:  use_defaults     <bool>     return empty instance of type,
         rather than none in the case that data is not present.
        param:  ignore_missing_directive <bool> whether an error should be
         raised in the case of a missing `robots.txt` file.
        '''
        self.user_agent = user_agent
        self.use_defaults = use_defaults
        self.upgrade_insecure = upgrade_insecure

        if not self.is_url(url_root):
            raise ValueError('{0} must be a valid url'.format(url_root))

        url = urllib.parse.urlparse(url_root)

        self.url_root = url.scheme + '://' + url.netloc
        self.robots_url = os.path.join(self.url_root, 'robots.txt')

        if \
        self.get_request(self.robots_url).status_code != 200 \
        and \
        self.ignore_missing_directive is False:
            raise ConnectionError('No `robots.txt` file found at {0}\nTo disable this behavior and treat all URLs as allowable, set the `ignore_missing_directive` arg to True'.format(self.robots_url))

        self.rp = urllib.robotparser.RobotFileParser()
        self.rp.set_url(self.robots_url)
        self.rp.read()


    @staticmethod
    def is_url(url):
        '''
        returns True:
            http://www.example.com/
            https://www.example.com/path
            https://www.example.com?param=something

        returns False:
            /relative/path
            #AnchorTag
            www.missing-schema.com
            partial.com
        '''
        try:
            result = urllib.parse.urlparse(url)
            return all([result.scheme, result.netloc])
        except ValueError:
            return False


    @staticmethod
    def netloc(url):
        '''
        arg:     https://www.google.com/search?query=hello
        returns: www.google.com
        '''
        return urllib.parse.urlparse(url).netloc


    @staticmethod
    def remove_duplicates(lst):
        '''
        Strips duplicate items from a list, non-mutatively
        '''
        if not isinstance(lst, list):
            raise TypeError('{0} not a valid list'.format(lst))
        return list(dict.fromkeys(lst))


    @staticmethod
    def pour_soup(response):
        '''
        Convenience function to create a BeautifulSoup object
        '''
        from bs4 import BeautifulSoup
        html = response.content
        parser = 'html.parser'
        soup = BeautifulSoup(html, parser)
        return soup


    def same_site(self, link):
        '''
        Checks whether the link points to an internal location
        '''
        nl_1 = self.netloc(self.url_root)
        nl_2 = self.netloc(link)
        return True if nl_1 == nl_2 else False


    def is_allowed(self, url):
        '''
        Checks robots.txt parser to see if url is allowed.
        '''
        generic_user_agent = '*'
        return self.rp.can_fetch(generic_user_agent, url)


    def get_request(self, url):
        if self.upgrade_insecure and urllib.parse.urlparse(url).scheme == 'http':
            url = url.replace('http', 'https')
        headers = {'User-Agent': self.user_agent}
        response = requests.get(url, headers=headers)
        return response


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


    def match(self, url):
        '''
        Used by the Selector class to determine whether or not the parser
        is capable of handling the provided URL. Returns a boolean value.
        '''
        return self.same_site(url)


    def info(self, pretty=True):
        '''
        Expands on the behavior of __dict__ method to display robots.txt directives.
        '''
        from pprint import pformat
        data = self.__dict__
        data['rp'] = str(data.get('rp'))
        if pretty:
            return pformat(data)
        return data

    # # @allowed ((class method decorator))
    # def allowed(foo):
    #     '''
    #     Decorator that will raise an error in the case that the
    #     URL provided as argument is disallowed based on robots.txt
    #     '''
    #     def magic(self):
    #         print("start magic")
    #         is_allowed(self)
    #         print(self.url_root)
    #         print("end magic")
    #     return magic
