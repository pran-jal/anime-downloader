import subprocess

def downloader(url, name) :
    s = 'ffmpeg -i "%s" -c copy %s.mp4' %(url, name)
    subprocess.run(["powershell", "-command", s] )