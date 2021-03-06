import sys
sys.path.insert(1, './src')
import htmlreader
import requests as r

def get_servers(url) :
    site = r.get(url).text
    read = htmlreader.reader()
    read.feed(site)
    read.close()
    return read.servers

if __name__ == '__main__':
    print(get_servers(input()))