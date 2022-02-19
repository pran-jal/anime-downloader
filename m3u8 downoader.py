import subprocess

a = input("Link : ")
n = input("Name : ")

s = 'ffmpeg -i "%s" -c copy %s.mp4' %(a, n)

subprocess.run(["powershell", "-command", "Start-Process PowerShell -ArgumentList '%s; PowerShell -NoExit'" %(s)] )
