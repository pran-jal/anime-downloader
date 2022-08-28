import requests as r
from src.heavenreader import reader
from seleniumwire import webdriver
# import seleniumwire.undetected_chromedriver as uc
# from seleniumwire.undetected_chromedriver import FirefoxOptions
# from seleniumwire.webdriver import FirefoxOptions

def get_json(urls: list, server_name = None):
    option = webdriver.FirefoxOptions()
    option.headless = True
    option.accept_insecure_certs = True
    browser = webdriver.Firefox(executable_path = 'webdriver\geckodriver', service_log_path='./webdriver/animeheaven_json.log')
    # browser = uc.Chrome(executable_path='webdriver\chromedriver', service_log_path='./webdriver/animeheaven_json.log', options=option )
    json_list = {}
    
    try:
        for url in urls:
            count = 0
            print('getting: ', url)
            browser.get(url)
            found = 0

            while True:
                for req in browser.requests:
                    if req.url.startswith('https://vidstream.pro/mediainfo/'):
                        a = r.get(req.url, params=req.params, headers=req.headers)
                        if a.status_code == 200 and a.json()["status"] == 200:
                            json_list[url] = a
                            # print(a.content)
                            found = 1
                            del browser.requests
                if found:
                    break
                if count == 1:
                    break
                else:
                    read = reader()
                    read.feed(browser.page_source)
                    server_list = read.servers
                    browser.switch_to.frame(browser.find_element_by_id("iframe-embed"))
                    count = +1
                    read.feed(browser.page_source)
                    if read.page_error:
                        browser.switch_to.parent_frame()
                        try:
                            add = browser.find_element_by_xpath("/html/div")
                            while True:
                                browser.execute_script("""
                                    var e = arguments[0];
                                    e.remove();
                                    """, add)
                                add = browser.find_element_by_xpath("/html/div")
                        except Exception as t:
                            pass
                        browser.find_element_by_id(server_list[next(iter(server_list))]['id']).find_element_by_xpath("./..").click()
                        print('error',server_list[next(iter(server_list))]['id'])    
    
    except Exception as e:
        print(e)
    
    finally:
        browser.quit()
        return json_list

if __name__ == '__main__':
    print(get_json('https://animeheaven.pro/watch/the-fruit-of-evolution-before-i-knew-it-my-life-had-it-made-KDnP-episode-2/'))

    