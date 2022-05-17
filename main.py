import os
import urls
import threading
import subprocess
import resolution
import downloader
import requests as r
from html.parser import HTMLParser as parser

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Connection': 'keep-alive',
    'origin': 'https://animeheaven.pro',
    'Referer': 'https://animeheaven.pro/',
}


quality = {
    'vidstream': {
    '1080': 'hls/1080/1080.m3u8',
    '720': 'hls/720/720.m3u8',
    '480': 'hls/480/480.m3u8',
    '360': 'hls/360/360.m3u8',
    },

    'mcloud': {
    '1080': 'hls/1080/1080.m3u8',
    '720': 'hls/720/720.m3u8',
    '480': 'hls/480/480.m3u8',
    '360': 'hls/360/360.m3u8',
    },

    'vizcloud': {
        '1080': 'H4/v.m3u8',
        '720': 'H3/v.m3u8',
        '480': 'H2/v.m3u8',
        '360': 'H1/v.m3u8',
    }
}

class reader(parser):

    def __init__(self, *, convert_charrefs = False) :
        super().__init__(convert_charrefs=convert_charrefs)
        self.reset()
        self.recording = 0
        self.link = []
        self.episodes = []

        self.title = 0
        self.element = {}

    def handle_starttag(self, tag, attrs):
        if tag.lower() == 'a':
            for i,j in attrs :
                if i.lower() == 'class' and j.lower() == 'nav-link btn btn-sm btn-secondary link-item':
                    for i,j in attrs :
                        if i.lower() == 'data-embed':
                            self.link.append(j)

        elif tag.lower() == 'ul' and attrs[0][0] == 'class' and attrs[0][1] == 'nav':
            self.recording += 1

        elif tag.lower() == 'title' :
            self.title += 1
                
    def handle_endtag(self, tag ) :
        if tag.lower() == 'ul' and self.recording>0:
            self.recording -= 1
        
        elif tag.lower() == 'title' and self.title>0:
            self.title-=1

    def handle_data(self, data):
        if self.recording>0:
            self.episodes.append(data) if ( data !='\n' and data != '\n ') else None

        elif self.title>0 :
            self.element['name'] = data
            
        elif data.startswith("window.skey") :
            self.element['key'] = data.split("'")[1]

def namevarifier(name):
    for i in name:
        if i not in 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890_.' :
            j = name.index(i)
            if (name[j-1] == '_' and j>0) or j==0:
                name = name[:j:]+name[j+1::]
            else :
                name = name[:j:]+'_'+name[j+1::]
    return name

def servers(url) :
    site = r.get(url).text
    read = reader()
    read.feed(site)
    read.close()
    return [read.link, read.episodes]

def urls_generator(url, total_episodes):
    url = url[::-1]
    end = None
    for i in range(len(url)) :
        if url[i] == '-' :
            if url[:i:][::-1] == 'uncen/':
                end = '-uncen/'
            else:
                if end != '-uncen/':
                    end = '/'
                break 
    url = url[i::][::-1]
    urls = []
    for episode in total_episodes:
        urls.append( url + episode + end )
    return urls

def varify_urls(urls) :
    for url in urls:
        if r.head(url).status_code != 200:
            # headers['Host'] = url.split('/')[2]
            urls[urls.index(url)] = r.head(url).headers['Location']
    return urls

def getSkey(url) :
    # headers.headers['Host'] = url.split('/')[2]               why ?
    headers['Host'] = url.split('/')[2]             
    skey = r.get(url, headers=headers).text
    read = reader()
    read.feed(skey)
    read.close()
    return read.element

def downloader(url, name, dir_name, capture_output=False) :
    print("downloading ", name)
    s = 'cd %s; ffmpeg -i "%s" -c copy %s.mp4' %(dir_name, url, name)
    if subprocess.run(["powershell", "-command", s], capture_output=capture_output).returncode == 0:
        return (f"{name} downloaded successfully")
    else:
        return (f"downloading  {name} failed")

class Downloader():
    def download_episode(self, url, keys, dir_name, capture_output=False):
        required = servers(url)    # [ [vidstream url, mcloud url]  [ no of episodes ] ]
        embedurls = required[0]
        embedurls = varify_urls(embedurls)
        info = embedurls[0].split('/e/')
        listurl = info[0]+'/info/'+info[1]+'&skey='+keys['key']
        # headers['Referer'] = embedurls[0]
        lists = r.get(listurl, headers=headers)
        episode = lists.json()['media']['sources'][1]['file']
        res = resolution.resolutions(episode)
        episode = episode[::-1]
        for i in range(len(episode)) :
            if episode[i] == '/' :
                break
        episode = episode[i::][::-1]+res[0]
        name = namevarifier(url.split('/watch/')[1][:-1:])
        self.result = downloader(episode, name, dir_name, capture_output)

url = input("URL : ")

print("Getting Required files..........")
required = servers(url)
total_episodes = required[1][2:]
embedurls = varify_urls(required[0])
keys = getSkey(embedurls[0])             # skey same for both servers

print("Required files Ready............")
print("\nTotal number of Episodes to download: ", len(total_episodes))

all_urls = urls_generator(url, total_episodes)
dir_name = all_urls[0].split('/watch/')[1][:-1:].split('episode')[0][:-1:]
print("Downloading to: ", dir_name)
if not os.path.exists(dir_name):
    os.mkdir(dir_name)

threads = []
results = []
print("Starting Downloading............")
for i in all_urls:
        d = Downloader()
        t = threading.Thread(target = d.download_episode, args= (i, keys, dir_name, True) )
        t.start()
        threads.append(t)
        results.append(d)

for t in threads:
    t.join()

for t in threads:
    while t.is_alive():
        continue

for t in results:    
    print(t.result)