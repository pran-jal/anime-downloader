from html.parser import HTMLParser as parser

class htmlreader(parser):
    def __init__(self, *, convert_charrefs = False):
        super().__init__(convert_charrefs=convert_charrefs)
        self.reset()
        self.src = ''
        self.ul = 0
        self.mp4upload_data_count = 0
        self.servers = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str or None]]):
        if tag.lower() == 'iframe':
            for i,j in attrs:
                if i.lower() == 'src':
                    self.src = j
        
        elif tag.lower() == 'ul':
            for i,j in attrs:
                if i.lower() == 'class' and j.lower() == 'list-server-items':
                    self.ul += 1
    
        elif tag.lower() == 'li':
            if ('class', 'linkserver') in attrs:
                for i,j in attrs:
                    if i == 'data-video':
                        self.servers.append(j)
        
        elif tag.lower() == 'font':
            if ('color', 'red') in attrs:
                self.mp4upload_data_count += 1
    
    def handle_endtag(self, tag: str):
        pass

    def handle_data(self, data: str):
        if data.startswith('https://www.mp4upload.com/') and self.mp4upload_data_count:
            self.mp4upload_data = data
            self.mp4upload_data_count -= 1
