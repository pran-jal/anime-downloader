import requests as r

def resolutions(list_url):
    resos = r.get(list_url)
    return [i for i in resos.text.split('\n') if i.startswith('H') or i.startswith('h') ]

if __name__ == '__main__':
    print(resolutions(input()))