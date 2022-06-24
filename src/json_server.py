import time
import seleniumwire.undetected_chromedriver as uc
from seleniumwire.undetected_chromedriver import ChromeOptions
from seleniumwire import webdriver
import requests as r


def get_json(urls: list, server_name = None):
    option = ChromeOptions()
    option.headless = True
    option.accept_insecure_certs = True
    browser = webdriver.Firefox(executable_path = 'webdriver\geckodriver', service_log_path='./webdriver/animeheaven_json.log')
    # browser = uc.Chrome(executable_path='webdriver\chromedriver', service_log_path='./webdriver/animeheaven_json.log', options=option )
    json_list = []
    for url in urls:
        print('getting: ', url)
        browser.get(url)
        found = 0
        if server_name:
            browser.find_element_by_id(server_name).click()
            time.sleep(3)
        while True:
            for req in browser.requests:
                if req.url.startswith('https://vizcloud.store/mediainfo/'):
                    print(req.params)
                    print(req.headers)
                    a = r.get(req.url, params=req.params, headers=req.headers)
                    if a.status_code == 200:
                        json_list.append({urls.index(url):a.json()})
                        found = 1
            if found:
                break
            browser.refresh()
            time.sleep(5)

if __name__ == '__main__':
    print(get_json('https://animeheaven.pro/watch/the-fruit-of-evolution-before-i-knew-it-my-life-had-it-made-KDnP-episode-2/'))

    