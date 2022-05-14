import subprocess
from typing import List

def run_command_with_progress(cmd, name):

    download = subprocess.Popen(
        cmd,
        universal_newlines=False,
        stderr=subprocess.STDOUT,
        stdout=subprocess.PIPE,
        stdin=subprocess.PIPE,  # Apply stdin isolation by creating separate pipe.
    )

    yield 0 

    while True:
        if download.stdout is None:
            continue
        line = download.stdout.readline().decode("utf-8", errors="replace").strip()
        if line == "" and download.poll() is not None:
            break
        if line.startswith('Duration: '):
            total_duration = line.split(', ')[0][10:]
            total_dur = int(total_duration[0:2]) * 60 * 60 + int(total_duration[3:5]) * 60 + int(total_duration[6:8])
            break
        
    while True:
        if download.stdout is None:
            continue
        if line == "" and download.poll() is not None:
            break 
        if line.startswith('out_time='):
            progress_time = line[9:]
            elapsed_time = int(progress_time[0:2]) * 60 * 60 + int(progress_time[3:5]) * 60 + int(progress_time[6:8])
            yield ('{0:.1f}').format(elapsed_time / total_dur * 100)
        line = download.stdout.readline().decode("utf-8").strip()

    if download.returncode != 0:
        raise RuntimeError("Error running command {}: {}\ndownloading  {} failed".format(cmd, download.stdout.readline(), name))

    yield 100

def progress_bar(cmd, name):
    for progress in run_command_with_progress(cmd, name):
        p = 'Progress :'
        s = 'Completed'
        fill = chr(9608)
        filled = int(float(progress))
        bar = fill*filled+'-'*(100-filled)
        print(f"{p} | {bar} | {progress}% {s}\r", end='\r')

def downloader(url, name, dir_name) :
    print("downloading ", name)
    cmd = ('ffmpeg -i %s -c copy %s.mp4 -progress -' %(url, name)).split(' ')
    progress_bar(cmd, name)
    return (f"{name} downloaded successfully")


if __name__ == '__main__':
    cmd = "ffmpeg -i https://ekerp.vidstream.pro/EqPVIPsMXV322yVezviuGdNz9wsVp_2yQlow5Od52MBlQ9QQTX4s9b01nxn7C_yI+tzdG4991O3U7fRtBiOikmeZRvMNGbxfRJCivXxFIkYzNJElHAMylNGatA_UoiuaZhmiX1o4myn55zkboURBwqd_was4TwHgws2BU8ys+ujdBJgglkyR2tpbM5GXU9Bbb58/br/hls/1080/1080.m3u8 -c copy teasing_master_takagi_san_season_3_dub_Q62r_episode_2.mp4 -progress -"
    cmd = cmd.split(' ')
    progress_bar(cmd, 'lol')