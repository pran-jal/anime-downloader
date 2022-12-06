import sys
sys.path.insert(1, "./")
import requests as r
from src.zororeader import reader
from servers import streamtape

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
    return read.epi_names, read.data_ids

def get_episode_servers(episode_id):
    servers = r.get(episode_servers_api + episode_id, headers=user_agent).json()["html"]
    read = reader()
    read.feed(servers)
    servers_ids = read.server_ids

    servers = []
    for id in servers_ids["sub"]:
        servers.append(r.get(episodes_servers_links_api + id, headers=user_agent).json()["link"])
    return servers
        


def main(url = None):
    if url == None:
        url = input("url: ")
    episodes_name_list, episodes_url_list = get_all_urls(url)
    
    episodes = []
    for i in episodes_url_list:
        print("getting link: ", episodes_name_list[i])
        servers = get_episode_servers(episodes_url_list[i])
        for server in servers:
            if 'streamtape' in server:
                episode = {}
                episode["url"] = server
                episode["title"] = episodes_name_list[i]
                episode["down_link"] = streamtape.get(server)
                episodes.append(episode)
            else:
                # print(f"Error: {episodes_name_list[i]} streamtape link not found. Zoro currently supports streamtape server only")
                print(server)

    print(episodes)

if __name__ == "__main__":
    main()