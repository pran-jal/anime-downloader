import requests as r
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Connection': 'keep-alive',
    'Host': 'kowxv.vidstream.pro',
    'origin': 'https://vizcloud.cloud',
    'Referer': 'https://vizcloud.cloud/',
}


def resolutions(list_url):
    resos = r.get(list_url, headers=headers)
    return [i for i in resos.text.split('\n') if i.startswith('H') or i.startswith('h') ]

if __name__ == '__main__':
    print(resolutions(input()))