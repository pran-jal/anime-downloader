import re
import sys
import base36
import requests as r
sys.path.insert(1, "./")

from src.utils.downloader import download
from src.readers.pahe import reader
from src.utils.titlecheck import validate

headers = {
    'referer': 'https://animepahe.com/',
    'origin': 'https://kwik.cx',
    'referer': 'https://kwik.cx/'
}

user_agent = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.102 Safari/537.36'
}


def e(c, a):    
    first = '' if c<a else str(len(e(c//a, a)))
    c=c%a
    c = chr(c+29) if c>35 else base36.dumps(c)
    return first + c

def chunk_decoder(session):
    session = session.split(');\',')
    p = re.findall(r"\w{1,2}://.*/\w{1,2}.\w{1,2}", session[0])[0]
    session = session[1].split(',')
    a = int(session[0])
    c = int(session[1])
    k = session[2].split('\'.split')[0][1:].split('|')
    d = {}
    while c:
        c-=1
        d[e(c,a)] = k[c]if k[c] else e(c,a)
    for something in d:
        p = re.sub(rf"\b{something}\b", d[something], p)
    return p


def all_epi_url(url):
    """ Depricated """
    episode_page = r.get(url).text
    read = reader()
    read.feed(episode_page)
    episode_list = read.episode_list
    session_ids = {}
    total_episodes = len(episode_list)
    for i in range(total_episodes):
        session_ids[i+1] = episode_list[i].split('/').pop()
    return session_ids


def season_key(url):
    url = url.split('/')
    if len(url)<5:
        raise ValueError("season_id Not Found. Invalid URL")
    return url[4]



def all_epi_url_from_api(url):         # this can bypass the use of pahereader, may be faster
    season_id = season_key(url)
    api_url = f"https://animepahe.com/api?m=release&id={season_id.split('?')[0]}&sort=episode_asc&"
    session_ids = {}
    page="page=1"
    
    while page:
        page = page.split('?').pop()
        print(api_url + page)
        session_ids_json = r.get(api_url + page, headers=user_agent)
        session_ids_json = session_ids_json.json()
        page = session_ids_json["next_page_url"]
        data = session_ids_json["data"]
        for item in data:
            session_ids[item["episode"]] = item["session"]

    return session_ids



def embeds_seperate(json_data):
    """ Depricated """
    eng = {}
    jpn = {}

    for item in json_data:
        print(item)
        for key, value in item.items():
            eval(value["audio"])[key] = value["kwik"]
        
    return jpn


def get_embed_urls(url):
    episode_page = r.get(url).text
    read = reader()
    read.feed(episode_page)
    read.close()
    return dict(read.resolution_list)


def main(url = None):
    if url == None:
        url = input("Url: ")
    season_id = season_key(url)
    sessions = all_epi_url_from_api(url)
    episodes = []
    print("total Episodes:", len(sessions))
    for id in sessions:
        print("getting link: ", id)
        episode = {}
        episode["url"] = f'https://animepahe.com/play/{season_id}/{sessions[id]}'
        
        embed_urls = get_embed_urls(episode['url'])['jpn']

        # .pop() the last value is the data of the best resolution.
        embed_page = r.get(embed_urls["1080"], headers=headers).text
        read = reader()
        read.feed(embed_page)
        episode["title"] = read.title.split(".mp4")[0]
        print(episode["title"])
        session_vala_chunk = re.findall(re.compile("<script>.*[\s\S]*?(?=</script>)"), embed_page)[0]
        
        
        """ 
        episode["title"] = validate(re.findall(re.compile("<title>[\w-]+.*.mp4</title>"), embed_page)[0].split('>')[1].split(".mp4")[0])
        session = session_vala_chunk.split('eval(function(').pop().split('|uwu|')[1].split("'.split('|')")[0].split('|')
        episode["down_link"] = session.pop() + "://" + session.pop() + "-" + session.pop() + "." + session.pop() + "." + session.pop() + "." + session.pop() + "/" + session.pop() + "/" + session.pop() + "/" + session.pop() + "/uwu.m3u8"
        """
        
        session = session_vala_chunk.split('}(').pop()[:-3]
        episode["down_link"]  = chunk_decoder(session)
        episodes.append(episode)

    dir_name = episodes[0]["title"].split("_-_")[0]
    referer = 'https://kwik.cx/'

    print("Required files Ready............")
    print("Downloading to {0}\n".format(dir_name))
    download(episodes, dir_name, referer)

if __name__ == "__main__":
    # main("https://animepahe.com/anime/d11b2a1a-64af-7a38-d006-67d87cf34b2b")
    main()