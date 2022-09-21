import re
import requests as r
from html.parser import HTMLParser as parser

class reader(parser):
    def __init__(self, *, convert_charrefs: bool = ...) -> None:
        super().__init__(convert_charrefs=convert_charrefs)
        self.reset()
        
        self.script = ''
        self.isscript = 0

    def handle_starttag(self, tag, attrs):
        if tag.lower() == 'script':
            self.isscript = 1

    def handle_endtag(self, tag):
        if tag.lower() == 'script':
            self.isscript = 0
    
    def handle_data(self, data):
        if self.isscript:
            if data.startswith("document"):
                self.script = data


user_agent = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.102 Safari/537.36'
}

def streamtape(url: str) -> str:

    url = "https://shavetape.cash/e/" + url.split("/e/")[1] 
    # url = re.sub(re.compile("/(http:|https:)(^|\/\/)(.*?\/)/"), "https://shavetape.cash/", url)
    page = r.get(url, headers=user_agent)

    if  not page.status_code>=200 and not page.status_code<=300:
        return("page not fetched")

    read = reader()
    read.feed(page.text)
    scripts = read.script.strip().split(';')
    scripts.pop()

    for script in scripts:
        url_parts = script.strip().split('innerHTML = ')[1].split("')")
        url_part = url_parts[0].split(" ('")
        start = re.sub(r"^(/)+", '', re.sub(re.compile("[\"+\\\' \(\)]+"), '', url_part[0]))
        end = url_parts[1].split('.substring(')
        buff = sum([int(i[0]) for i in end if len(i) and i[0].isnumeric])
        url = "https://" + start + url_part[1][buff:]
        down_link = r.head(url).headers.get("Location")
        if down_link.endswith("/video.mp4"):
            return down_link   

if __name__ == "__main__":
    print(streamtape("https://streamtape.com/e/948lZQgkwKUa3Da/"))