from html.parser import HTMLParser as parser

class reader(parser):

    def __init__(self, *, convert_charrefs = False) :
        super().__init__(convert_charrefs=convert_charrefs)
        self.reset()
        self.link = []
        self.recording = 0
        self.episodes = []

        self.element = {}
        self.title = 0

    def handle_starttag(self, tag, attrs):
        if tag.lower() == 'a':
            for i,j in attrs :
                if i.lower() == 'class' and j.lower() == 'nav-link btn btn-sm btn-secondary link-item':
                    for i,j in attrs :
                        if i.lower() == 'data-embed':
                            self.link.append(j)

        if tag.lower() == 'ul' and attrs[0][0] == 'class' and attrs[0][1] == 'nav':
            self.recording += 1

        if tag.lower() == 'title' :
            self.title += 1
                
    def handle_endtag(self, tag ) :
        if tag.lower() == 'ul' and self.recording>0:
            self.recording -= 1
        
        if tag.lower() == 'title' and self.title>0:
            self.title-=1

    def handle_data(self, data):
        if self.recording>0:
            self.episodes.append(data) if ( data !='\n' and data != '\n ') else None

        if self.title>0 :
            self.element['name'] = data
            
        if data.startswith("window.skey") :
            self.element['key'] = data.split("'")[1]
