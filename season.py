import os
import threading
import src.urls as urls
import src.episode_list as episode_list
import src.resolution as resolution
import src.namevarifier as namevarifier
import src.progress_bar as progress_bar
import src.json_server as json_server

class Downloader():
    def __init__(self, url) -> None:
        self.epi_url = url
        self.name = ''
    
    def download_episode(self, dir_name, lists):
        episode = lists.json()['data']['media']['sources'][1]['file']
        res = resolution.resolutions(episode)
        episode = episode[::-1]
        for i in range(len(episode)) :
            if episode[i] == '/' :
                break
        episode = episode[i::][::-1]+res[0]
        self.name = namevarifier.namevarifier(self.epi_url.split('/watch/')[1][:-1:])
        self.bar = progress_bar.ProgressBar(episode, self.name, dir_name)
        self.bar.downloader()


def main(url=None):
    if url == None:
        url = input("URL : ")

    total_episodes = len(episode_list.get_e_list(url))-2

    all_urls = urls.generator(url, total_episodes)

    dir_name = all_urls[0].split('/watch/')[1][:-1:].split('episode')[0][:-1:]
    print("Downloading to {0}\n".format(dir_name))
    
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)

    lists = json_server.get_json(all_urls)
    threads = []
    results = []
    for url in lists:
        d = Downloader(url)
        t = threading.Thread(target = d.download_episode, args=(dir_name, lists[url]))
        t.start()
        threads.append(t)
        results.append(d)

    print("Required files Ready............")
    wait_for = 0
    total_in_downloading = len(results)
    result = ['']*total_in_downloading
    while wait_for < total_in_downloading:
        try:
            for t in range(total_in_downloading):
                success = f"{results[t].name} downloaded successfully\r"
                fail = f"downloading {results[t].name} failed\r"
                new_result = results[t].bar.progress
                if new_result in [success, fail] and new_result != result[t]:
                    wait_for += 1
                result[t] = new_result

            print('\n\n\033[2K'.join(result), end=f'\033[{2*len(results)-2}A\033[2K')

        except Exception as e:
            pass

    print('\033[2K', end='')
    print('\n\n\033[2K'.join(result))


if __name__ == '__main__' :
    main()
