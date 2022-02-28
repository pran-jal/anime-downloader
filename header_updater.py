from email import header
import headers

def updater(host):
    if host == 'vidstream':
        headers.headers['Host'] = 'vidstream.pro'
    elif host == 'mcloud':
        headers.headers['Host'] = 'mcloud.to'
