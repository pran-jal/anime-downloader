import requests as r
import headers
import jsonread


url = jsonread.url()
skey = r.get(url=url, headers=headers)

print(skey.text)