import threading
from turtle import down
import requests as r
import servers
import skey
import resolution
import urls
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
        res = resolution.resolutions(episode)
        episode = episode[::-1]
        for i in range(len(episode)) :
            if episode[i] == '/' :
                break
        episode = episode[i::][::-1]+res[0]
        name = namevarifier.namevarifier(url.split('/watch/')[1][:-1:])
        self.result = downloader.downloader(episode, name, capture_output)

url = input()

print("Getting Required files..........")
required = servers.servers(url)
total_episodes = len(required[1])-2
embedurls = embed_varify.varify_urls(required[0])
keys = skey.getSkey(embedurls[0])        # skey same for both servers

print("Required files Ready............")
all_urls = urls.generator(url, total_episodes)

threads = []
results = []
print("Starting Downloading............")
for i in all_urls:
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

