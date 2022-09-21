import re
import sys
sys.path.insert(1, "./")
import requests as r
from src.zororeader import reader

host = "https://zoro.to"
episode_list_api = "https://zoro.to/ajax/v2/episode/list/"
episode_servers_api = "https://zoro.to/ajax/v2/episode/servers?episodeId="
episodes_servers_links_api = "https://zoro.to/ajax/v2/episode/sources?id="
user_agent = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.102 Safari/537.36'
}

def captcha():
    pass

def get_all_urls(url: str):
    anime_id = url.split('?')[0].split('-')[-1]
    all_url_html = r.get(episode_list_api + anime_id, headers=user_agent)
    read = reader()
    read.feed(all_url_html.json()["html"])
    return read.data_ids

def get_episode_servers(episode_id):
    servers = r.get(episode_servers_api + episode_id, headers=user_agent).json()["html"]
    read = reader()
    read.feed(servers)
    servers_ids = read.server_ids

    servers = []
    for id in servers_ids:
        servers.append(r.get(episodes_servers_links_api + id).json()["link"])

    return servers
        


def main(url = None):
    if url == None:
        url = input("url: ")
    episodes_url_list = get_all_urls(url)
    
    for i in episodes_url_list:
        servers = get_episode_servers(episodes_url_list[i])
        for server in servers:
            print(server)
            # data = r.get(server + "?z=&autoPlay=1&oa=0&asi=1", headers = {
            #     'referer': 'https://zoro.to/',
            #     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.102 Safari/537.36'
            #     }
            # )
            # print(data.text)
        print()
        # break

if __name__ == "__main__":
    main("https://zoro.to/watch/fullmetal-alchemist-brotherhood-1?ep=1")