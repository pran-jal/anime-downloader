import headers
import requests as r


def lists(source) :
    del headers.headers['Referer']
    headers.headers['Host'] =     source.split('/')[2]
    return r.get(source, headers=headers.headers)
