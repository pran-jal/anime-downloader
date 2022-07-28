from html.parser import HTMLParser as parser

class reader(parser):

    def __init__(self, *, convert_charrefs = False) :
        super().__init__(convert_charrefs=convert_charrefs)
        self.reset()
        
        self.recording = 0
        self.link = []
        self.episodes = []
        self.watch_ids = {}
        self.servers = {}
        self.title = 0
        self.page_error = 0
        self.episode_name = ''

        self.page_identifier = ''

    def handle_starttag(self, tag, attrs):
        if tag.lower() == 'a':
            for i,j in attrs :
                if i.lower() == 'class' and j.lower() == 'nav-link btn btn-sm btn-secondary link-item':
                    server = {}
                    for i,j in attrs :
                        if i.lower() == 'data-embed':
                            server['embed'] = j
                            server['key'] = j.split('/e/')[1].split('?')[0]
                        elif i.lower() == 'id':
                            server['id'] = j
                    if server != {}:
                        self.servers[server['embed'].split('/e/')[0].split('//')[1].split('.')[0]] = server

        elif tag.lower() == 'ul' and attrs[0][0] == 'class' and attrs[0][1] == 'nav':
            self.recording += 1

        elif tag.lower() == 'title' :
            self.title = 1
        
        elif tag.lower() == 'div' :
            for i, j in attrs :
                if i.lower() == 'class' and j.lower() == 'detail_page-watch':
                    for i, j in attrs :
                        if i.lower() == 'data-mid':
                            self.page_identifier = j
                            # why is page identifier same for all episodes of a season
                
                elif i.lower() == 'class' and j.lower() == 'errorpage':
                    self.page_error = 1
    def handle_endtag(self, tag ) :
        if tag.lower() == 'ul' and self.recording>0:
            self.recording -= 1
        
        elif tag.lower() == 'title' and self.title>0:
            self.title-=1

    def handle_data(self, data):
        if self.recording>0:
            self.episodes.append(data) if ( data !='\n' and data != '\n ') else None

        elif self.title>0 :
            self.episode_name = data
            self.title = 0
        
        # Obsolete. website does not use skey now
        elif data.startswith("window.skey") :
            self.element['key'] = data.split("'")[1]
