import sys
import os
sys.path.insert(1, './src')
import subprocess

def downloader(url, epi_name, dir_name, capture_output=True) :
    print("downloading ", epi_name)
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)
    s = 'ffmpeg -i "%s" -c copy %s.mp4 -y' %(url, epi_name)
    a = subprocess.run(s, cwd=dir_name, capture_output=capture_output).returncode
    if a == 0:
        return (f"{epi_name} downloaded successfully")
    else:
        return (f"downloading {epi_name} failed")
        
if __name__ == '__main__' : 
    downloader(input(), 'download.mp4', True)