import sys
sys.path.insert(1, './src')
import namevarifier
import progress_bar
import resolution
import json_server

def download_episode(url):
    lists = json_server.get_json([url])
    # print(lists)
    episode = lists.json()['data']['media']['sources'][1]['file']
    res = resolution.resolutions(episode)
    episode = episode[::-1]
    for i in range(len(episode)) :
        if episode[i] == '/' :
            break
    episode = episode[i::][::-1]+res[0]
    name = namevarifier.namevarifier(url.split('/watch/')[1][:-1])
    bar = progress_bar.ProgressBar(episode, name, name)
    bar.downloader()
    # return progress_bar.downloader(episode, name, name)


if __name__ == '__main__' :
    print(download_episode(input()))