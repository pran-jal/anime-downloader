from html.parser import HTMLParser as parser

class reader(parser):

    def __init__(self, *, convert_charrefs = False) :
        super().__init__(convert_charrefs=convert_charrefs)
        self.reset()
        self.data_ids = {}
        self.epi_servers = {}
        self.epi_names = {}
        self.is_server = 0
        self.server_ids = { "sub" : [], "dub": [] }

    def handle_starttag(self, tag, attrs) -> None:
        if tag.lower() == 'a':
            for i, j in attrs:
                if i == "data-number":
                    for o, k in attrs:
                        if o == "data-id":
                            self.data_ids[j] = k
                
                        elif o == 'title':
                            self.epi_names[j] = k
                            

        elif tag.lower() == "div":
            for i, j in attrs:
                if i == "class" and j == "item server-item":
                    self.server_ids[attrs[1][1]].append(attrs[2][1])

    def handle_data(self, data):
        if self.is_server and len(data.strip()): 
            self.epi_servers[data] = self.data_id
            self.is_server = 0