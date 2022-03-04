import subprocess

def downloader(url, name, capture_output=False) :
    print("downloading ", name)
    s = 'ffmpeg -i "%s" -c copy %s.mp4' %(url, name)
    if subprocess.run(["powershell", "-command", s], capture_output=capture_output).returncode == 0:
        return (name, "downloading successfully")
    else:
        return ("downloading ", name, " failed")


if __name__ == '__main__' : 
    downloader('https://mmxpl.vidstream.pro/EqPVJvsPWF322yVezviuGdNz9wsVp_2yQlow5Od52MBlQ9QQHH4h9fsymRbkFPyI+tzdG4991OzQ7PRgBCOikmeZRvMMHb1fSZKivXxFIkYzNJElHAAylNGaugrUoS2cZhCiT0Q97y6R+D0UtVNAz6N2wakqWALvnsKGV8Sh9+zKF5NgyE6Mk81ZPdqIEpxDacxb/br/hls/1080/1080.m3u8', 'test', False)