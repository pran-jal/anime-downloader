import requests as r
import headers

def varify_urls(urls) :
    for url in urls:
        if r.get(url, headers=headers.headers).status_code != 200:
            headers.headers['Host'] = url.split('/')[2]
            urls[urls.index(url)] = r.head(url).headers['Location']
    return urls

if __name__ == "__main__" :
    print(varify_urls([input()]))