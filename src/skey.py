import requests as r
import headers
import htmlreader

def getSkey(url) :
    """ 
    Get Skey for a episode. Skey works same for whole
    season.

    obsolete.
    ( episode or season not use this anymore. )
    """
    headers.headers['Host'] = url.split('/')[2]               
    skey = r.get(url, headers=headers.headers).text
    read = htmlreader.reader()
    read.feed(skey)
    read.close()
    return read.element

# FOR mcloud change host to -> 'Host': 'mcloud.to'
if __name__ == '__main__' :
    print(getSkey(input()))