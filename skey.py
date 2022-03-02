import requests as r
import headers
from html.parser import HTMLParser

class MyHTMLParser(HTMLParser):
    def __init__(self, convert_charrefs = False ) :
        super().__init__(convert_charrefs=convert_charrefs)
        self.reset()
        self.element = {}
        self.title = 0
    
    def handle_starttag(self, tag, attrs):
        if tag.lower() == 'title' :
            self.title += 1

    def handle_endtag(self, tag: str):
        if tag.lower() == 'title' and self.title>0:
            self.title-=1

    def handle_data(self, data) :
        if self.title>0 :
            self.element['name'] = data
            
        if data.startswith("window.skey") :
            self.element['key'] = data.split("'")[1]

def getSKEY(url) :
    skey = r.get(url, headers=headers.headers).text
    parser = MyHTMLParser()
    parser.feed(skey)
    return parser.element


# FOR mcloud change host to -> 'Host': 'mcloud.to'
