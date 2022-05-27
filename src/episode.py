import sys
sys.path.insert(1, './src')
import requests as r
import embed_varify
import servers 
import get_info
import namevarifier
import downloader
import headers
import resolution

def download_episode(url, capture_output=False):
    required = servers.servers(url)    # [ [vidstream url, mcloud url]  [ no of episodes ] ]
    embedurls = required[0]
    embedurls = embed_varify.varify_urls(embedurls)
    keys = get_info.get_key(embedurls[0])
    info = embedurls[0].split('/e/')
    listurl = info[0]+'/info/'+keys
    lists = r.get(listurl, headers=headers.headers)
    episode = lists.json()['data']['media']['sources'][1]['file']
    res = resolution.resolutions(episode)
    episode = episode[::-1]
    for i in range(len(episode)) :
        if episode[i] == '/' :
            break
    episode = episode[i::][::-1]+res[0]
    name = namevarifier.namevarifier(url.split('/watch/')[1])
    return downloader.downloader(episode, name, capture_output)

if __name__ == '__main__' :
    print(download_episode(input()))