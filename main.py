import os
import threading
import subprocess
import requests as r
from seleniumwire import webdriver
from html.parser import HTMLParser as parser
# import seleniumwire.undetected_chromedriver as uc
# from seleniumwire.undetected_chromedriver import FirefoxOptions
# from seleniumwire.webdriver import FirefoxOptions

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Connection': 'keep-alive',
    'origin': 'https://animeheaven.pro',
    'Referer': 'https://animeheaven.pro/',
}

quality = {
    'vidstream': {
    '1080': 'hls/1080/1080.m3u8',
    '720': 'hls/720/720.m3u8',
    '480': 'hls/480/480.m3u8',
    '360': 'hls/360/360.m3u8',
    },

    'mcloud': {
    '1080': 'hls/1080/1080.m3u8',
    '720': 'hls/720/720.m3u8',
    '480': 'hls/480/480.m3u8',
    '360': 'hls/360/360.m3u8',
    },

    'vizcloud': {
        '1080': 'H4/v.m3u8',
        '720': 'H3/v.m3u8',
        '480': 'H2/v.m3u8',
        '360': 'H1/v.m3u8',
    }
}

class reader(parser):

    def __init__(self, *, convert_charrefs = False) :
        super().__init__(convert_charrefs=convert_charrefs)
        self.reset()
        
        self.recording = 0
        self.link = []
        self.episodes = []
        self.watch_ids = {}
        self.servers = {}
        self.title = 0
        self.page_error = 0
        self.episode_name = ''
        self.page_identifier = ''

    def handle_starttag(self, tag, attrs):
        
        if tag.lower() == 'a':
            for i,j in attrs :
                if i.lower() == 'class' and j.lower() == 'nav-link btn btn-sm btn-secondary link-item':
                    server = {}
                    for i,j in attrs :
                        if i.lower() == 'data-embed':
                            server['embed'] = j
                            server['key'] = j.split('/e/')[1].split('?')[0]
                        elif i.lower() == 'id':
                            server['id'] = j
                    if server != {}:
                        self.servers[server['embed'].split('/e/')[0].split('//')[1].split('.')[0]] = server
                    del server

        elif tag.lower() == 'ul' and attrs[0][0] == 'class' and attrs[0][1] == 'nav':
            self.recording += 1

        elif tag.lower() == 'title' :
            self.title = 1
        
        elif tag.lower() == 'div' :
            for i, j in attrs :
                if i.lower() == 'class' and j.lower() == 'detail_page-watch':
                    for i, j in attrs :
                        if i.lower() == 'data-mid':
                            self.page_identifier = j
                            # why is page identifier same for all episodes of a season
                
                elif i.lower() == 'class' and j.lower() == 'errorpage':
                    self.page_error = 1
    
    def handle_endtag(self, tag ) :
        if tag.lower() == 'ul' and self.recording>0:
            self.recording -= 1
        
        elif tag.lower() == 'title' and self.title>0:
            self.title-=1

    def handle_data(self, data):
        if self.recording>0:
            self.episodes.append(data) if ( data !='\n' and data != '\n ') else None

        elif self.title>0 :
            self.episode_name = data
            self.title = 0
        
        # Obsolete. website does not use skey now
        elif data.startswith("window.skey") :
            self.element['key'] = data.split("'")[1]

def get_json(urls: list, server_name = None):
    option = webdriver.FirefoxOptions()
    option.headless = True
    option.accept_insecure_certs = True
    browser = webdriver.Firefox(executable_path = 'webdriver\geckodriver', service_log_path='./webdriver/animeheaven_json.log')
    # browser = uc.Chrome(executable_path='webdriver\chromedriver', service_log_path='./webdriver/animeheaven_json.log', options=option )
    json_list = {}
    try:
        for url in urls:
            count = 0
            print('getting: ', url)
            browser.get(url)
            found = 0

            while True:
                for req in browser.requests:
                    if req.url.startswith('https://vizcloud.site/mediainfo/'):
                        a = r.get(req.url, params=req.params, headers=req.headers)
                        if a.status_code == 200 and a.json()["status"] == 200:
                            json_list[url] = a
                            found = 1
                            del browser.requests
                if found:
                    break
                if count == 1:
                    break
                else:
                    read = reader()
                    read.feed(browser.page_source)
                    server_list = read.servers
                    browser.switch_to.frame(browser.find_element_by_id("iframe-embed"))
                    count = +1
                    read.feed(browser.page_source)
                    if read.page_error:
                        browser.switch_to.parent_frame()
                        try:
                            add = browser.find_element_by_xpath("/html/div")
                            while True:
                                browser.execute_script("""
                                    var e = arguments[0];
                                    e.remove();
                                    """, add)
                                add = browser.find_element_by_xpath("/html/div")
                        except Exception as t:
                            pass
                        browser.find_element_by_id(server_list[next(iter(server_list))]['id']).find_element_by_xpath("./..").click()
                        print('error',server_list[next(iter(server_list))]['id'])    
    
    except Exception as e:
        print(e)
    
    finally:
        browser.quit()
        return json_list

def namevarifier(name):
    for i in name:
        if i not in 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890_.' :
            j = name.index(i)
            if (name[j-1] == '_' and j>0) or j==0:
                name = name[:j:]+name[j+1::]
            else :
                name = name[:j:]+'_'+name[j+1::]
    return name

def get_e_list(url) :
    site = r.get(url).text
    read = reader()
    read.feed(site)
    read.close()
    return read.episodes

def urls_generator(url, total_episodes):
    url = url[::-1]
    end = None
    for i in range(len(url)) :
        if url[i] == '-' :
            if url[:i:][::-1] == 'uncen/':
                end = '-uncen/'
            else:
                if end != '-uncen/':
                    end = '/'
                break 
    url = url[i::][::-1]
    urls = []
    for i in range(1, total_episodes+1):
        urls.append( url+str(i)+end )
    return urls

def resolutions(list_url):
    resos = r.get(list_url)
    return [i for i in resos.text.split('\n') if i.startswith('H') or i.startswith('h') ]

def downloader(url, name, dir_name, capture_output=True) :
    print("downloading ", name)
    s = 'cd %s; ffmpeg -i "%s" -c copy %s.mp4 -y' %(dir_name, url, name)
    if subprocess.run(["powershell", "-command", s], capture_output=capture_output).returncode == 0:
        return (f"{name} downloaded successfully")
    else:
        return (f"downloading  {name} failed")

class Downloader():
    def download_episode(self, url, dir_name, lists, capture_output = True):
        episode = lists.json()['data']['media']['sources'][1]['file']
        res = resolutions(episode)
        episode = episode[::-1]
        for i in range(len(episode)) :
            if episode[i] == '/' :
                break
        episode = episode[i::][::-1]+res[0]
        name = namevarifier(url.split('/watch/')[1][:-1:])
        self.result = downloader(episode, name, dir_name, capture_output)

def main(url=None):
    if url == None:
        url = input("URL : ")

    total_episodes = len(get_e_list(url))-2

    all_urls = urls_generator(url, total_episodes)

    lists = get_json(all_urls)
    print("Required files Ready............")

    dir_name = all_urls[0].split('/watch/')[1][:-1:].split('episode')[0][:-1:]
    print("\nDownloading to {0}".format(dir_name))
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)

    threads = []
    results = []

    for url in lists:
        d = Downloader()
        t = threading.Thread(target = d.download_episode, args=(url, dir_name, lists[url]))
        t.start()
        threads.append(t)
        results.append(d)
    
    for t in threads:
        t.join()

    for t in threads:
        while t.is_alive():
            continue

    for t in results:    
        print(t.result)

if __name__ == '__main__' :
    main()
