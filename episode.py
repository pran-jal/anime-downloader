import requests as r
import servers
import skey
import headers

def download_episode(url):

    required = servers.servers(url)    # [ [vidstream , mcloud url]  [ no of episodes ] ]

    servers_list = required[0]
    total_no_episodes = required[1].pop()

    keys = skey.getSkey(servers_list[0])        # skey same for both servers

    for i in servers_list :
        info = i.split('/e/')
        host = info[0][8::]
        listurl = info[0]+'/info/'+info[1]+'&skey='+keys['key']
        headers.headers['Host'] = host
        headers.headers['Referer'] = i
        print(r.get(listurl, headers=headers.headers).json()['media']['sources'])

download_episode(input())