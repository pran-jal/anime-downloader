import requests as r
import headers

def sources(url, embedurl) :
    headers.headers['Referer'] = embedurl
    lists = r.get(url, headers=headers.headers)
    return lists