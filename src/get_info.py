from selenium import webdriver
import requests
import re

def get_key(url):
    domain = url.split('/e/')[0]
    url = '/e/' + url.split('/e/')[1]
    a = requests.get(domain+url).text
    for line in a.split('\n'):
        if line.startswith('<script type="text/javascript" src="/assets/vidstream/cache/scripts.js?v='):
            script_src = line.split('src="')[1][:-11:]
            script = requests.get(domain+script_src).text
            lol = re.finditer("return\x20[\w\d_]+\['[\w]+'\]\['[\w]+'\]\(this\['[\w]+'\]\)", script)
            for match in lol:
                strmatch = match.group().split(' ')[1]
                new_script = script[:match.start()] + "alert(" + strmatch + ")" + script[match.end():]
    
            options = webdriver.FirefoxOptions()
            options.add_argument('-headless')
            browser = webdriver.Firefox(executable_path='./webdriver/geckodriver.exe')
            browser.get(domain + url)
            browser.execute_script(new_script)
            infoKey = browser.switch_to.alert.text
            browser.switch_to.alert.accept()
            browser.quit()
            
    return infoKey

if __name__ == '__main__':
    print(get_key('https://vizcloud.cloud/e/RLJQM7OZ7P59?domain=animeheaven.pro'))