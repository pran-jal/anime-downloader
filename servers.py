import htmlreader
import requests as r

def servers(url) :
    site = r.get(url).text
    read = htmlreader.reader()
    read.feed(site)
    read.close()
    return [read.link, read.episodes]

if __name__ == '__main__':
    print(servers(input()))