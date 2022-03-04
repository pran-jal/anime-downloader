import requests as r
import servers
import skey
import downloader
import headers

def download_episode(url):

    required = servers.servers(url)    # [ [vidstream url, mcloud url]  [ no of episodes ] ]
    embedurl = required[0]
    total_no_episodes = required[1].pop()
    keys = skey.getSkey(embedurl[0])        # skey same for both servers
    info = embedurl[0].split('/e/')
    listurl = info[0]+'/info/'+info[1]+'&skey='+keys['key']
    headers.headers['Referer'] = embedurl[0]
    lists = r.get(listurl, headers=headers.headers)
    episode = lists.json()['media']['sources'][1]['file']
    episode = episode[::-1]
    for i in range(len(episode)) :
        if episode[i] == '/' :
            break

    episode = episode[i::][::-1]+'hls/1080/1080.m3u8'
    return episode

print(download_episode(input()))