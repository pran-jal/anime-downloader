from html.parser import HTMLParser
import requests as r
import json


class MyHTMLParser(HTMLParser):

    def __init__(self, *, convert_charrefs = False) :
        super().__init__(convert_charrefs=convert_charrefs)
        self.reset()
        self.link = {}

    def handle_data(self, data) :
        try:
            if data[1] == '{' and data[0] != '{' :
                self.link = data
        except:
            1


def embedUrl(url=None) :
    site = r.get(url).text
    parser = MyHTMLParser()
    parser.feed(site)
    return (json.loads(parser.link)['@graph'][0]['video']['embedUrl'] )
