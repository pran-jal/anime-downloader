import subprocess

def downloader(url, name, dir_name, capture_output=False) :
    print("downloading ", name)
    s = 'cd %s; ffmpeg -i "%s" -c copy %s.mp4' %(dir_name, url, name)
    if subprocess.run(["powershell", "-command", s], capture_output=capture_output).returncode == 0:
        return (f"{name} downloaded successfully")
    else:
        return (f"downloading  {name} failed")


if __name__ == '__main__' : 
    downloader(input(), 'download.mp4', False)