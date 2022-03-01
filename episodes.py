import requests as r
import servers
import old.skey as skey
import old.m3u8_downloader as m3u8_downloader

def download_episodes(url):

    required = servers.embedUrl(url)    # [ [vidstream , mcloud url]  [ no of episodes ] ]

    total_no_episodes = required[1].pop()
    servers_list = required[0]
    keys = skey.getSKEY(servers_list[0])        # skey same for both servers


    info = servers_list[0].split('/e/')
    listurl = info[0]+'/info/'+info[1]+'&skey='+keys['key']

    print(listurl)
download_episodes(input())