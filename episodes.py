import requests as r
import servers
import old.skey as skey
import old.m3u8_downloader as m3u8_downloader

def download_episodes(url):

    details = servers.embedUrl(url)
    total_no_episodes = details[1].pop()
    servers_list = details[0]
    keys = skey.getSKEY(servers_list[0])


    info = servers_list[0].split('/e/')
    listurl = info[0]+'/info/'+info[1]+'&skey='+keys['key']


    print(m3u8_downloader.m3u8_downloader(url, keys['name']))

download_episodes(input())