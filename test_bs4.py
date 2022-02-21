import requests as r
import file_write
from bs4 import BeautifulSoup as bs

# url = input("URL : ")
url = "https://animeheaven.pro/watch/food-wars-the-third-plate-lV8Z-episode-8/"

site = r.get(url)
index = site.text
headers = site.headers

html_doc = bs(index, 'html.parser')

try :
    result = file_write.fileWrite(html_doc.find(type="application/ld+json").contents[0])
    if result !=None :
        print("Failed to write Json to file")
        print(f"Error : {result}")
    else :
        print("JSON saved successfully")
except Exception as e:
    print(e)



