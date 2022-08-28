import os
import sys
sys.path.insert(1,'./')
import requests as r
import src.json_server as json_server
from src.titlecheck import validate
from src.resolution import resolutions
from src.heavenreader import reader
from src.downloader import download

def get_epi_list(url) :
    site = r.get(url).text
    read = reader()
    read.feed(site)
    read.close()
    return read.episodes_url

def generate(url, total_episodes):
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
    for i in range(1, total_episodes+1):
        urls.append( url+str(i)+end )
    return urls

def main(url=None):
    if url == None:
        url = input("Url : ")

    all_urls = get_epi_list(url)

    dir_name = validate(url.split('/watch/')[1][:-1:].split('episode')[0][:-1:])
    lists = json_server.get_json(all_urls)
    episodes = []
    for url in lists:
        episode = {}
        episode["url"] = url
        episode["name"] = validate(url.split('/watch/')[1][:-1])
        m3u8 = lists[url].json()['data']['media']['sources'][1]['file']
        res = resolutions(m3u8)
        m3u8 = m3u8[::-1]
        for i in range(len(m3u8)) :
            if m3u8[i] == '/' :
                break
        m3u8 = m3u8[i::][::-1]+res[0]
        episode["down_link"] = m3u8
        episodes.append(episode)

    print("Required files Ready............")
    print("Downloading to {0}\n".format(dir_name))
    # download(episodes, dir_name)

if __name__ == '__main__' :
    main()
