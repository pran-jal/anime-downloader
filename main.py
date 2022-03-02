
import requests as r
import embedUrl
import skey
import sources
import threading
import json
import m3u8_downloader
import lists

def download(url, no) :
    embedurl = embedUrl.embedUrl(url)
    print("embedUrl generated")
   
    Skey = skey.getSKEY(embedurl)
    print("Skey generated")

    info = embedurl.split('/e/')
    print("info ready")

    listurl = info[0]+'/info/'+info[1]+'&skey='+Skey['key']
    print("list url ready")
    
    sourcess = sources.sources(listurl, embedurl)
    print("sources ready")
    source = json.loads(sourcess.text)['media']['sources'][1]['file']
    print("source ready")
    quality = lists.lists(source).text.split('\n')
    print("quality ready")

    length = len(quality)
    i = 0
    while i<length :
        if not quality[i].startswith('hls/') :
            quality.remove(quality[i])
            i-=1
            length-=1
        i+=1

    source = source[::-1]

    for i in range(len(source)) :
        if source[i] == '/' :
            break
    episode = source[i::][::-1]+quality[0]

    print(m3u8_downloader.m3u8_downloader(episode, no))
