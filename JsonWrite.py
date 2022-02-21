from html.parser import HTMLParser
import requests as r
import file_write


class MyHTMLParser(HTMLParser):
    def handle_data(self, data) :
        try:
            if data[1] == '{' and data[0] != '{' :
                result = file_write.fileWrite(data)
                if result !=None :
                    print("Failed to write Json to file")
                    print(f"Error : {result}")
        except:
            1


def JsonWrite(url=None) :
    url = "https://animeheaven.pro/watch/food-wars-the-third-plate-lV8Z-episode-8/"
    site = r.get(url).text
    parser = MyHTMLParser()
    parser.feed(str(site))