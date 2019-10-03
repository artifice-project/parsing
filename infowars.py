from base import BaseParser


class InfowarsParser(BaseParser):

    def __init__(self, url_root, rude=True):
        super().__init__(url_root, rude=True)

    def parse_title(self, soup):
        return soup.title.text or ''

    def parse_text(self, soup):
        p_tags = [e.get_text() for e in soup.find_all('p', {})]
        article = '\n'.join(p_tags)
        washed = " ".join(article.split())
        return str(washed)

    def parse_captions(self, soup):
        captions = []
        for p in soup.find_all('p'):
            try:
                if 'caption' in p['class']:
                    captions.append(p.text)
            except:
                pass
        return captions

    def parse_links(self, soup):
        all_links = self.remove_duplicates(
            [str(link.get('href')) for link in soup.find_all('a')]
        )
        strained_links = self.strain_links(all_links)
        return strained_links
