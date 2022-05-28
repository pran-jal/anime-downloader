import subprocess

def downloader(url, name, capture_output=False) :
    print("downloading ", name)
    s = 'ffmpeg -i "%s" -c copy %s.mp4 -y' %(url, name)
    if subprocess.run(["powershell", "-command", s], capture_output=capture_output).returncode == 0:
        print('done')
        return (f"{name} downloaded successfully")
    else:
        print('failed')
        return (f"downloading  {name} failed")

if __name__ == '__main__' : 
    downloader(input(), 'download.mp4', False)