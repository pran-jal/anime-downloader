import sys
sys.path.insert(1, './src')
import htmlreader
import requests as r

def get_e_list(url) :
    site = r.get(url).text
    read = htmlreader.reader()
    read.feed(site)
    read.close()
    return read.episodes

if __name__ == '__main__':
    print(get_e_list(input()))