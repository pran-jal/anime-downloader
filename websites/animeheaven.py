import os
import sys
sys.path.insert(1,'./')
import threading
import src.urls as urls
import src.episode_list as episode_list
import src.json_server as json_server
import src.episode as episode

def main(url=None):
    if url == None:
        url = input("URL : ")

    total_episodes = len(episode_list.get_e_list(url))-2

    all_urls = urls.generator(url, total_episodes)

    dir_name = all_urls[0].split('/watch/')[1][:-1:].split('episode')[0][:-1:]
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)
    print("Downloading to {0}\n".format(dir_name))

    lists = json_server.get_json(all_urls)
    threads = []
    results = []
    for url in lists:
        d = episode
        t = threading.Thread(target = d.download_episode, args=(url, lists[url], dir_name,))
        t.start()
        threads.append(t)
        results.append(d)
    print("Required files Ready............")

    for t in threads:
        t.join()
    for t in threads:
        while t.is_alive():
            continue

if __name__ == '__main__' :
    main()
