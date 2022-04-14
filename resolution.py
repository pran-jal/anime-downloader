import requests as r

def resolutions(list_url):
    list = r.get(list_url)
    return [i for i in list.text.split('\n')  if i.startswith('h') ]

if __name__ == '__main__':
    print(resolutions(input()))