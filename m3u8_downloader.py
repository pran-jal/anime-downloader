import subprocess

def m3u8_downloader(url, name) :
    s = 'ffmpeg -i "%s" -c copy %s.mp4' %(url, name)
    subprocess.run(["powershell", "-command", "Start-Process PowerShell -ArgumentList '%s; PowerShell -NoExit'" %(s)] )
    return 'Downloading'