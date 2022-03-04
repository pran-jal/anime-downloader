import requests as r
import servers
import skey
import downloader
import headers

def download_episode(url):

    required = servers.servers(url)    # [ [vidstream url, mcloud url]  [ no of episodes ] ]

    servers_list = required[0]
    total_no_episodes = required[1].pop()
    keys = skey.getSkey(servers_list[0])        # skey same for both servers


download_episode(input())