import sys
import os
sys.path.insert(1, "./")
from src.ffmpeg import ffmpeg_downloader as ffmpeg
from src.curl import curl_downloader as curl

def download(episodes: list, dir_name, referer, use = None):
    if os.path.exists(dir_name):
        to_del = []
        for episode in episodes:
            if os.path.exists(dir_name + "/" + episode["title"] + ".mp4"):
                to_del.append(episode)

        if len(to_del):
            ans = input(f"Episodes already exists. Overwrite o | Skip s | Rename r ")
    
            if ans in ['o', 'O']:
                for episode in to_del:
                    episodes.remove(episode)
    
            elif ans in ['R', 'r']:
                for episode in episodes:
                    if episode in to_del:
                        while os.path.exists(dir_name + "/" + episode["title"] + ".mp4"):
                            episode["title"]+="(1)"
                            print(episode["title"])
        
            elif ans in ['S', 's']:
                episodes = [episode for episode in episodes if episode not in to_del]
    else:
        os.mkdir(dir_name)

    downloaders = []
    for episode in episodes:
        epi = ffmpeg(episode["down_link"], episode["title"], dir_name, referer)
        downloaders.append(epi)

    for downl in downloaders:
        downl.start_download()
        downl.track()

if __name__ == "__main__":
    download()