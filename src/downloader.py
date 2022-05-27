import sys
sys.path.insert(1, './src')
import subprocess
import progress_bar

def downloader(url, epi_name, dir_name, capture_output=False) :
    print("downloading ", epi_name)
    s = 'cd %s; ffmpeg -i "%s" -c copy %s.mp4' %(dir_name, url, epi_name)

    # command = 'ffmpeg -i %s -c copy %s.mp4 -progress -' %(url, epi_name)
    # cmd = command.split(' ')
    # bar = progress_bar.ProgressBar(cmd=cmd, epi_name=epi_name, dir_name=dir_name)
    # while True:
    #     for progress in bar.run_command_with_progress():
    #         bar.progress_Bar(progress)
    #     break
    # if bar.result == 0:
    #     return (f"{epi_name} downloaded successfully")
    # else:
    #     return (f"downloading {epi_name} failed")
    a = subprocess.run(s).returncode
    if a == 0:
        return (f"{epi_name} downloaded successfully")
    else:
        return (f"downloading {epi_name} failed")

if __name__ == '__main__' : 
    downloader(input(), 'download.mp4', False)