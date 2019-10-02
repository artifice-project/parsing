from base import BaseParser


class NPRParser(BaseParser):
    def __init__(self, url_root):
        super().__init__(url_root)

    def parse_title(self, soup):
        pass

    def parse_text(self, soup):
        pass

    def parse_captions(self, soup):
        pass

    def parse_links(self, soup):
        pass
