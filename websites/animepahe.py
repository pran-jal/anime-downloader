import re
import sys
import base36
import requests as r
sys.path.insert(1, "./")

from src.utils.downloader import download
from src.readers.pahe import reader
from src.utils.titlecheck import validate

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36',
    'Accept': '*/*',
    'Cookie': 'cf_clearance=uaBM.E5xHkoWKGzEAoxPfC46yCN2oSUlXNHAt1tYNck-1705145388-0-2-8471a20e.fc3293ae.d4b3d68f-0.2.1705145388; __ddgid_=ZouCeyh7ilQrjgQX; __ddg2_=weJsH1HcawaLxXZo; __ddg1_=i66CePRuMJ7DKMrGZYnH; res=1080; aud=jpn; av1=0; XSRF-TOKEN=eyJpdiI6ImZabTc4d0JjMmE1M3MvekNCZStURXc9PSIsInZhbHVlIjoia2RYcXZUSWMzR09tU2xlTnJjcnFidVd3S2VST1pMcWRkY3dtdnJiMlhEUEIzUmdGSEozSUkxK2puRnpVVFJIMVlDaXBhb0VoSXZDRzRJL0JLYzBFSEkwL1MwdTBrcCtQN1Y5dmczYlZJOXRPc0Vxd1ZHbkFRaVczYXlsWnllNFIiLCJtYWMiOiJmMmUzMzEzMDAxMzIwNmQyZjBhY2QyYzc0MWZiMDhkZDUwNjkwODkwNDAzNzM0MjgxMzBmODVkMDYxYTZiOWJlIiwidGFnIjoiIn0^%^3D; laravel_session=eyJpdiI6IjhJdzMzdVB3R0Y4ZXNwYjVBMHZJcUE9PSIsInZhbHVlIjoiZmdDOEV6K3hrclVnRU5NQmZHZlF0NGZpL0xGMXJEZ2JnbXlOdHdCUVQxZlpweCtnaGR0OG1vY2prUC9nUlBZaHVVWlYwMHFRS2FmRHFpTllGS1Bocm9RUWNPR3FWcGd2MCtwOHFzR1o4dXZqVDRscGhYN25zNlZtTWx2ajZFSjIiLCJtYWMiOiIzOGZmMjkwN2U0MmVlM2JhMTAxNDBiN2YxYzkwMDVhNzI2ZjJlMzM5YWU5YjU1YmQ0NDM5YWFhNDk3MDcwZTFkIiwidGFnIjoiIn0^%^3D; SERVERID=janna; XSRF-TOKEN=eyJpdiI6IngvYkdhREw4OWdHeGhoV0NBMjNZMmc9PSIsInZhbHVlIjoiVHBkQ2d3WHN3Mkc4cUExc01qS1VXcWxVZWNIUXBEcjFsYW0wUkp6L2NXVUZqMU9hK2J6T005RUwza0xtY0Z5VkU5bU5FQ2l1M1JocW1FWVBzRjFjT0JEM0dIY1g3WmNJSS9rN0d4ZGhobER5UXZyTXB0UHlUZXppKzZ5ZU9rUjUiLCJtYWMiOiI1YTgxODBjNTRmYWYyZWEwMDgyZmY3ZjJhNWM2MGU2MGQ4OGU5ODY1MWI2OTJhY2Q1ZTdiN2YxMjk5ZWJmZTZkIiwidGFnIjoiIn0%3D; laravel_session=eyJpdiI6IjJIZXpxN1lqVEk5c2xGTUx4aVZJNGc9PSIsInZhbHVlIjoiMDJDWUxneDRMR2tzT2VGREVMWUZXWDI0Zml0aStDeGpESWVHUDlXOHNaVWZVSEI2N1orQ1NoK3NLV3VZeGNXdGlXTlNlRlRYcjRuaWwyVzhHOURXYmFibDRlT21vY0o3RW5EdEp2ajJFcGdLU01HVlAzbmZYRVpMQitWQk5BKzEiLCJtYWMiOiJjODdjNjJlMWEwMGY4OGY3MjY3MTg0ODQ4Njk4OTA3ODcyNzcxN2ZiN2FmMDFiNzFhZGE5ZmVmODk5NmUyYTg1IiwidGFnIjoiIn0%3D',
    'Host': 'animepahe.ru'
}

kwik_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36',
    'Accept': '*/*',
    'Cookie': 'cf_clearance=uaBM.E5xHkoWKGzEAoxPfC46yCN2oSUlXNHAt1tYNck-1705145388-0-2-8471a20e.fc3293ae.d4b3d68f-0.2.1705145388; __ddgid_=ZouCeyh7ilQrjgQX; __ddg2_=weJsH1HcawaLxXZo; __ddg1_=i66CePRuMJ7DKMrGZYnH; res=1080; aud=jpn; av1=0; XSRF-TOKEN=eyJpdiI6ImZabTc4d0JjMmE1M3MvekNCZStURXc9PSIsInZhbHVlIjoia2RYcXZUSWMzR09tU2xlTnJjcnFidVd3S2VST1pMcWRkY3dtdnJiMlhEUEIzUmdGSEozSUkxK2puRnpVVFJIMVlDaXBhb0VoSXZDRzRJL0JLYzBFSEkwL1MwdTBrcCtQN1Y5dmczYlZJOXRPc0Vxd1ZHbkFRaVczYXlsWnllNFIiLCJtYWMiOiJmMmUzMzEzMDAxMzIwNmQyZjBhY2QyYzc0MWZiMDhkZDUwNjkwODkwNDAzNzM0MjgxMzBmODVkMDYxYTZiOWJlIiwidGFnIjoiIn0^%^3D; laravel_session=eyJpdiI6IjhJdzMzdVB3R0Y4ZXNwYjVBMHZJcUE9PSIsInZhbHVlIjoiZmdDOEV6K3hrclVnRU5NQmZHZlF0NGZpL0xGMXJEZ2JnbXlOdHdCUVQxZlpweCtnaGR0OG1vY2prUC9nUlBZaHVVWlYwMHFRS2FmRHFpTllGS1Bocm9RUWNPR3FWcGd2MCtwOHFzR1o4dXZqVDRscGhYN25zNlZtTWx2ajZFSjIiLCJtYWMiOiIzOGZmMjkwN2U0MmVlM2JhMTAxNDBiN2YxYzkwMDVhNzI2ZjJlMzM5YWU5YjU1YmQ0NDM5YWFhNDk3MDcwZTFkIiwidGFnIjoiIn0^%^3D; SERVERID=janna; XSRF-TOKEN=eyJpdiI6IngvYkdhREw4OWdHeGhoV0NBMjNZMmc9PSIsInZhbHVlIjoiVHBkQ2d3WHN3Mkc4cUExc01qS1VXcWxVZWNIUXBEcjFsYW0wUkp6L2NXVUZqMU9hK2J6T005RUwza0xtY0Z5VkU5bU5FQ2l1M1JocW1FWVBzRjFjT0JEM0dIY1g3WmNJSS9rN0d4ZGhobER5UXZyTXB0UHlUZXppKzZ5ZU9rUjUiLCJtYWMiOiI1YTgxODBjNTRmYWYyZWEwMDgyZmY3ZjJhNWM2MGU2MGQ4OGU5ODY1MWI2OTJhY2Q1ZTdiN2YxMjk5ZWJmZTZkIiwidGFnIjoiIn0%3D; laravel_session=eyJpdiI6IjJIZXpxN1lqVEk5c2xGTUx4aVZJNGc9PSIsInZhbHVlIjoiMDJDWUxneDRMR2tzT2VGREVMWUZXWDI0Zml0aStDeGpESWVHUDlXOHNaVWZVSEI2N1orQ1NoK3NLV3VZeGNXdGlXTlNlRlRYcjRuaWwyVzhHOURXYmFibDRlT21vY0o3RW5EdEp2ajJFcGdLU01HVlAzbmZYRVpMQitWQk5BKzEiLCJtYWMiOiJjODdjNjJlMWEwMGY4OGY3MjY3MTg0ODQ4Njk4OTA3ODcyNzcxN2ZiN2FmMDFiNzFhZGE5ZmVmODk5NmUyYTg1IiwidGFnIjoiIn0%3D',
    'Referer': 'https://animepahe.ru/'

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


def embeds_seperate(json_data):
    """ Depricated. to avoid use of "eval" """
    eng = {}
    jpn = {}

    for item in json_data:
        for key, value in item.items():
            eval(value["audio"])[key] = value["kwik"]
        
    return jpn


def season_key(url):
    url = url.split('/')
    if len(url)<5:
        raise ValueError("season_id Not Found. Invalid URL")
    return url[4]


def all_epi_url_from_api(url):         # this can bypass the use of pahereader, may be faster
    season_id = season_key(url)
    api_url = f"https://animepahe.ru/api?m=release&id={season_id.split('?')[0]}&sort=episode_asc&"
    session_ids = {}
    page="page=1"
    
    while page:
        page = page.split('?').pop()
        print(api_url + page)
        session_ids_json = r.get(api_url + page, headers=headers)

        if session_ids_json.status_code != 200:
            raise Exception("Episodes URL fetch failed")
        
        session_ids_json = session_ids_json.json()
        page = session_ids_json["next_page_url"]
        data = session_ids_json["data"]
        for item in data:
            session_ids[item["episode"]] = item["session"]

    return session_ids


def get_embed_urls(url):

    episode_page = r.get(url, headers=headers).text
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
        episode["url"] = f'https://animepahe.ru/play/{season_id}/{sessions[id]}'
        
        embed_urls = get_embed_urls(episode['url'])['jpn']

        # .pop() the last value is the data of the best resolution.
        embed_page = r.get(embed_urls["1080"], headers=kwik_headers).text
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
    # https://animepahe.ru/anime/16fcd4e3-fa59-85b0-57cf-f1c28ff3e0d4
    # https://animepahe.ru/anime/203d1657-a85b-daab-a169-ff5ecb0b14fa
    # https://animepahe.ru/anime/f2bd56b5-2e02-ac22-44f6-85afdd0f42a1
    # https://animepahe.ru/anime/b9acebfe-ca23-12c8-50b6-4d43af3010dc
    # https://animepahe.ru/anime/24fdcd85-eb50-1175-9e34-a44f3d5da7a8
    main()