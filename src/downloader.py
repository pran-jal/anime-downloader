# from curl import curl_downloader as curl
import sys
import os
sys.path.insert(1, "./")
from src.ffmpeg import ffmpeg_downloader as ffmpeg

def download(episodes: list, dir_name, referer, use = None):
    print(episodes)
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
                        episode["title"]+="(1)"
        
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
    
    while True:
        for downl in downloaders:
            print(downl.progress)

if __name__ == "__main__":
    download([{'title': 'tsubasa-to-hotaru-2016-60bq-episode-1', 'down_link': 'https://pvjdk.vidstream.pro/GqOPIvgJT0Km0WQZzrmqQI1u9hZKurPiVRFyrOM9z4diQ9IQHD98t6ojwVOlTeyJ84jKHYJ8xO3b6fNtECWvhmaUQP9bE+pbSpGgvmBGL0cwOo8rRwE4w8+T7wfPoimZckP2T1Mj5VqWkCIRukRfyrh+wKRoF2i52f6UU8qo8PzP/br/hls/720/720.m3u8'}, {'title': 'tsubasa-to-hotaru-2016-60bq-episode-2', 'down_link': 'https://dbrzk.vidstream.pro/GqOPIv8GT0Km0WQZzrmqQI1u9hZKurO2VRZyq_o2jIEiQ9IQHD98t6ojwVOlTeyJ84jKHYJ8xO3b6fNtECWvhmaUQP9bE+pbSpGgvmBGL0cwOo8rRwE4w8+T7wfPoimZckP2T1Mj5VqWkCIRukRfyrh+wKRoF2i52f6UU8qo8PzP/br/hls/720/720.m3u8'}, {'title': 'tsubasa-to-hotaru-2016-60bq-episode-3', 'down_link': 'https://vjbxb.vidstream.pro/GqOPIv8PT0Km0WQZzrmqQI1u9hZKurOxVUVy96RhxcchQ9IQHD98t6ojwVOlTeyJ84jKHYJ8xO3b6fNtECWvhmaUQP9bE+pbSpGgvmBGL0cwOo8rRwE4w8+T7wfPoimZckP2T1Mj5VqWkCIRukRfyrh+wKRoF2i52f6UU8qo8PzP/br/hls/720/720.m3u8'}], "tsubasa-to-hotaru-2016-60bq")