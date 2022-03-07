import requests as r
import threading
import skey
import embed_varify
import headers
import servers
import downloader
import concurrent.futures

url = input()

url = url[::-1]
for i in range(len(url)) :
    if url[i] == '-' :
        break
url = url[i::][::-1]

urls = []
for i in range(1, 10):
    urls.append(url+f"{i}/")
print(urls)

embedurls = []
for i in urls :
    with concurrent.futures.ThreadPoolExecutor() as executor:
        embedurls.append(executor.submit(servers.servers, i).result()[0][0])
print(embedurls)

embedurls = embed_varify.varify_urls(embedurls)


skey = skey.getSkey(embedurls[0])['key']
print(skey)

for i in embedurls:
    info = i.split('/e/')
    listurl = info[0]+'/info/'+info[1]+'&skey='+skey
    headers.headers['Referer'] = i
    embedurls[embedurls.index(i)] = r.get(listurl, headers=headers.headers).json()['media']['sources'][1]['file']
print(embedurls)

episodes = []
for i in embedurls:
   episodes.append(i[:-9:]+'hls/1080/1080.m3u8')
print(episodes)

threads = []

for i in episodes :
    name = urls[episodes.index(i)].split('/watch/')[1][:-1:]
    t = threading.Thread(target=downloader.downloader, args=(i, name, True))
    threads.append(t)
    t.start()

for i in threads:
    i.join()

for i in threads:
    while i.is_alive():
        continue
    