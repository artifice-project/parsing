from base import BaseParser


class NPRParser(BaseParser):
    def __init__(self, url_root):
        super().__init__(url_root)

    def parse_title(cls, soup):
        pass

    def parse_text(cls, soup):
        pass

    def parse_captions(cls, soup):
        pass

    def parse_links(cls, soup):
        pass
