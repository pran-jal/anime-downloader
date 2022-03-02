import subprocess

def m3u8_downloader(url, name) :
    s = 'ffmpeg -i "%s" -c copy %s.mp4 -y' %(url, name)
    subprocess.run(["powershell", "-command", f'Start-Process PowerShell -ArgumentList \'-NoExit {s}\' '] )