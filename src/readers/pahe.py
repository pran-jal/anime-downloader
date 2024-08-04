from html.parser import HTMLParser as parser

class reader(parser):
    def __init__(self, *, convert_charrefs = False) :
        super().__init__(convert_charrefs=convert_charrefs)
        self.reset()
        self.list_div = 0
        self.res_menu = 0
        self.episode_list = []
        self.resolution_list = {'jpn': {}, 'eng': {}, "chi": {}}
        self.title_found = 0

    def handle_starttag(self, tag, attrs):
        if tag.lower()=='div':
            for i,j in attrs:
                if i.lower() == 'id':
                    
                    if j.lower() == 'resolutionmenu':
                        self.res_menu = 1
                    
                    elif j.lower() == 'scrollarea':
                        self.list_div = 1


        elif tag.lower() == 'a' and self.list_div:
            for i,j in attrs:
                if i.lower() == 'href':
                    self.episode_list.append(j)

        elif tag.lower() == 'button' and self.res_menu:
            self.resolution_list[attrs[4][1]][attrs[3][1]] = attrs[1][1]

        elif tag.lower() == 'title':
            self.title_found = 1
    
    def handle_endtag(self, tag):
        if tag.lower() == 'div':
            self.list_div = 0
        
    def handle_data(self, data):
        if self.title_found:
            self.title = data
            self.title_found = 0
