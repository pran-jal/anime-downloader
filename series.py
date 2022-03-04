from html.parser import HTMLParser as parser
import requests as r
import skey
import threading
import servers
import concurrent.futures

url = input()

url = url[::-1]
for i in range(len(url)) :
    if url[i] == '-' :
        break
url = url[i::][::-1]

urls = []
for i in range(1, 9):
    urls.append(url+f"{i}/")
print(urls)

embedurls = []
""" threads = []
for i in urls :
    t = threading.Thread(target=servers.servers, args=(i,))
    threads.append(t)
    t.start()
    embedurls.append([0][0]) 
print(embedurls) """

for i in urls :
    with concurrent.futures.ThreadPoolExecutor() as executor:
        embedurls.append(executor.submit(servers.servers, i).result()[0][0])
print(embedurls)

print()
skeys = []
for i in embedurls :
    skeys.append(skey.getSkey(i))
for i in skeys :
    print(i['name'], i['key'])

print()


skeys_1 = []
for i in embedurls :
    with concurrent.futures.ThreadPoolExecutor() as executor:
        skeys_1.append(executor.submit(skey.getSkey, i).result())
for i in skeys_1:
    print(i['name'], i['key'])


