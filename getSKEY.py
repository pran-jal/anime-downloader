import requests as r
import headers
import jsonread
from html.parser import HTMLParser

class MyHTMLParser(HTMLParser):
    def __init__(self, convert_charrefs = False ) :
        super().__init__(convert_charrefs=convert_charrefs)
        self.reset()
        self.element = {}
    
    def handle_starttag(self, tag, attrs):
        if tag.lower() == 'title' :
            self.element['name'] = tag

    def handle_data(self, data) :
        if data.startswith("window.skey") :
            self.element['key'] = data.split("'")[1]

def getSKEY() :
    url = jsonread.url()
    skey = r.get(url, headers=headers.headers).text
    parser = MyHTMLParser()
    parser.feed(skey)
    return parser.element