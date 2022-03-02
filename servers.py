from html.parser import HTMLParser
import requests as r

class MyHTMLParser(HTMLParser):

    def __init__(self, *, convert_charrefs = False) :
        super().__init__(convert_charrefs=convert_charrefs)
        self.reset()
        self.link = []
        self.recording = 0
        self.episodes = []

    def handle_starttag(self, tag, attrs):
        if tag.lower() == 'a':
            for i,j in attrs :
                if i.lower() == 'class' and j.lower() == 'nav-link btn btn-sm btn-secondary link-item':
                    for i,j in attrs :
                        if i.lower() == 'data-embed':
                            self.link.append(j)

        if tag.lower() == 'ul' and attrs[0][0] == 'class' and attrs[0][1] == 'nav':
            self.recording += 1
                
    def handle_endtag(self, tag ) :
        if tag.lower() == 'ul' and self.recording>0:
            self.recording -= 1

    def handle_data(self, data):
        if self.recording>0:
            self.episodes.append(data) if ( data !='\n' and data != '\n ') else None


def embedUrl(url=None) :
    site = r.get(url).text
    parser = MyHTMLParser()
    parser.feed(site)
    parser.close()
    return [parser.link, parser.episodes]