
class Selector(object):
    '''
    Automatically select the appropriate parser based on the supplied URL.
    Behavior can be set for the case where no match exists, and can be
    either a raised error, or simply returning a None type object.
    '''
    def __init__(self, *parsers, no_match_raises_error=True):
        self.parsers = [*parsers]
        self.no_match_raises_error = no_match_raises_error


    def match(self, url):
        '''
        Returns the appropriate parser for the provided URL. Behavior when
        no match exists defaults to `no_match_raises_error` attribute value.
        '''
        for parser in self.parsers:
            if parser.match(url):
                return parser
        if self.no_match_raises_error:
            raise Exception('No matching parser found for {}\nParsers: {}'.format(url, self.parsers))
        else:
            pass


    def scrape(self, parser, url):
        '''
        1. Checks if URL is allowed based on robots.txt
        2. GET request to the URL
        3. Extracts content
        returns: content <dict>
        '''
        allowed = parser.is_allowed(url)
        if not allowed:
            return
        response = parser.get_request(url)
        data = parser.extract_content(response)
        return data
