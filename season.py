import threading
from turtle import down
import requests as r
import servers
import skey
import namevarifier
import downloader
import headers
import embed_varify

class Downloader():
    def download_episode(self, url, keys, capture_output=False):
        required = servers.servers(url)    # [ [vidstream url, mcloud url]  [ no of episodes ] ]
        embedurls = required[0]
        embedurls = embed_varify.varify_urls(embedurls)
        info = embedurls[0].split('/e/')
        listurl = info[0]+'/info/'+info[1]+'&skey='+keys['key']
        headers.headers['Referer'] = embedurls[0]
        lists = r.get(listurl, headers=headers.headers)
        episode = lists.json()['media']['sources'][1]['file']
        episode = episode[::-1]
        for i in range(len(episode)) :
            if episode[i] == '/' :
                break
        episode = episode[i::][::-1]+'hls/1080/1080.m3u8'
        name = namevarifier.namevarifier(url.split('/watch/')[1][:-1:])
        self.result = downloader.downloader(episode, name, capture_output)

url = input()

print("Getting Required files..........")
required = servers.servers(url)
total_episodes = int(required[1].pop())+1
embedurls = embed_varify.varify_urls(required[0])
keys = skey.getSkey(embedurls[0])        # skey same for both servers
print("Required files Ready............")

url = url[::-1]
for i in range(len(url)) :
    if url[i] == '-' :
        break
url = url[i::][::-1]

print("Starting Downloading............")

urls = []
for i in range(1, total_episodes):
    urls.append(url+f"{i}/")

threads = []
results = []
for i in urls:
    d = Downloader()
    t= threading.Thread(target = d.download_episode, args= (i, keys, True) )
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

