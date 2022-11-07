import re
import sys
import requests as r
sys.path.insert(1, './')

from src.downloader import download
from src.pahereader import reader
from src.titlecheck import validate

headers = {
    'referer': 'https://animepahe.org/',
    'origin': 'https://kwik.cx',
    'referer': 'https://kwik.cx/'
}

user_agent = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.102 Safari/537.36'
}


def all_epi_url(url):
    episode_page = r.get(url).text
    read = reader()
    read.feed(episode_page)
    episode_list = read.episode_list
    session_ids = {}
    total_episodes = len(episode_list)
    for i in range(total_episodes):
        session_ids[i+1] = episode_list[i].split('/').pop()
    return session_ids

def all_epi_url_from_api(url):         # this can bypass the use of pahereader, may be faster
    url = url.split('/')
    
    if len(url)<5:
        raise ValueError("season_id Not Found. Invalid URL")
    
    season_id = url[4]
    api_url = f"{url[0]}" + "//" + f"{url[2]}/api?m=release&id={season_id.split('?')[0]}&sort=episode_asc&"
    session_ids = {}
    page="page=1"
    
    while page:
        page = page.split('?').pop()
        session_ids_json = r.get(api_url + page, headers=user_agent).json()
        page = session_ids_json["next_page_url"]
        data = session_ids_json["data"]
        for item in data:
            session_ids[item["episode"]] = item["session"]

    return session_ids

def embeds_seperate(json_data):
    eng = {}
    jpn = {}

    for item in json_data:
        for key, value in item.items():
            eval(value["audio"])[key] = value["kwik"]
        
    return jpn

def main(url = None):
    if url == None:
        url = input("Url: ")
    sessions = all_epi_url_from_api(url)
    episodes = []
    
    print("total Episodes:", len(sessions))
    for id in sessions:
        print("getting link: ", id)
        episode = {}
        episode["url"] = f'https://animepahe.com/api?m=links&id={sessions[id]}&p=kwik'
        embed_urls = embeds_seperate(r.get(episode["url"], headers=user_agent).json()['data'])# .pop() the last value is the data of the best resolution.
        embed_page = r.get(embed_urls["1080"], headers=headers).text
        episode["title"] = validate(re.findall(re.compile("<title>[\w-]+.mp4</title>"), embed_page)[0].split('>')[1].split(".mp4")[0])
        session_vala_chunk = re.findall(re.compile("<script>.*[\s\S]*?(?=</script>)"), embed_page)[0]
        session = session_vala_chunk.split('eval(function(').pop().split('|uwu|')[1].split("'.split('|')")[0].split('|')
        episode["down_link"] = session.pop() + "://" + session.pop() + "-" + session.pop() + "." + session.pop() + "." + session.pop() + "." + session.pop() + "/" + session.pop() + "/" + session.pop() + "/" + session.pop() + "/uwu.m3u8"
        episodes.append(episode)

    dir_name = episodes[0]["title"].split("_-_")[0]
    referer = 'https://kwik.cx/'

    download(episodes, dir_name, referer)

if __name__ == "__main__":
    # main("https://animepahe.com/anime/d11b2a1a-64af-7a38-d006-67d87cf34b2b")
    main()