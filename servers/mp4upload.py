import requests as r
import re
import heavenreader as heavenreader

def get(server):
    server_url = server.split('embed-')
    download_page = r.get(server_url[0]+server_url[1])
    if download_page.status_code == 200:
        download_link_regex = re.compile('<font\scolor="[\w]+">.*.mp4</font>')
        download_link = re.findall(download_link_regex, download_page.text)
        # print(download_link)
        reader = heavenreader()
        reader.feed(download_link[0])
        linktodownload = reader.mp4upload_data
        params={
            'op':'download2',
            'id':'0j8u9g6v9fnx',
            'rand':'',
            'referer':download_page.url,
            'method_free':'+',
            'method_premium':'',
        }
        header = {
            'Host': 'www.mp4upload.com',
            'Origin': 'https://www.mp4upload.com',
            'Referer': server,
            'Cookie': 'aff=389795; lang=english',
        }
        print(params)
        res = r.post(linktodownload, headers=header, data=params, allow_redirects=False)
        mp4_link = res.headers['location']
        cmd = f'curl.exe {mp4_link} -H "Referer: https://www.mp4upload.com/" -o name.mp4'