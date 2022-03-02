import requests as r
import headers
import htmlreader


def getSkey(url) :
    skey = r.get(url, headers=headers.headers).text
    read = htmlreader.reader()
    read.feed(skey)
    read.close()
    return read.element

# FOR mcloud change host to -> 'Host': 'mcloud.to'
