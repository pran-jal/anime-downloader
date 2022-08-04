import sys
sys.path.insert(1, './src')
import namevarifier
import downloader
import resolution
import json_server

def download_episode(url, lists, dir_name=None):
    episode = lists.json()['data']['media']['sources'][1]['file']
    res = resolution.resolutions(episode)
    episode = episode[::-1]
    for i in range(len(episode)) :
        if episode[i] == '/' :
            break
    episode = episode[i::][::-1]+res[0]
    name = namevarifier.namevarifier(url.split('/watch/')[1][:-1])
    if dir_name is None:
        dir_name = name
    return downloader.downloader(episode, name, dir_name, True)


if __name__ == '__main__' :
    url = input()
    print(download_episode(url, json_server.get_json([url])[url]))