import subprocess
import os

class ffmpeg_downloader:        
    def __init__(self, down_link, title, dir_name, referer, *args):
        self.cmd=['ffmpeg']+[*args]+['-referer', referer, '-i', down_link, '-c', 'copy', title+'.mp4', '-progress', '-']
        self.directory = dir_name
        self.title = title
        self.progress = 0
        self.state = None  # gives current condition of download
        # self.progress = f"{self.title}: |{'-'*50}| 0.0% Completed\r"
    
    def start_download(self):
        self.download = subprocess.Popen(
            self.cmd, 
            universal_newlines=False, 
            stderr=subprocess.STDOUT, 
            stdout=subprocess.PIPE, 
            stdin=subprocess.PIPE,
            cwd=self.directory
        )

    def track(self):
        while True:
            if self.download.stdout is None:
                continue
            line = self.download.stdout.readline().decode("utf-8").strip()
            if line == "" and self.download.poll() is not None:
                break
            if line.startswith('Duration: '):
                total_duration = line.split(', ')[0][10:]
                total_dur = int(total_duration[0:2]) * 60 * 60 + int(total_duration[3:5]) * 60 + int(total_duration[6:8])
                break
        
        while True:
            word = self.download.stdout.read(1).decode("utf-8")
            if word == "" and self.download.poll() is not None:
                break
            if word == '\n':
                line = ""
            else:
                line += word
            if line == f"File '{self.title}.mp4' already exists. Overwrite? [y/N] ":
                self.state = "waiting for overwrite conformation"
                self.download.stdin.write(bytes(input(line)+'\n', 'utf-8'))
                self.download.stdin.flush()
                break
            elif line.startswith('out_time='):      #this means that there is nothing to overwrite. i.e this is first download.
                break
        
        self.state = 'Downloading'
        while True:
            if self.download.stdout is None:
                continue
            line = self.download.stdout.readline().decode("utf-8").strip()
            if line == "" and self.download.poll() is not None:
                break 
            if line.startswith('out_time='):
                progress_time = line[9:]
                elapsed_time = int(progress_time[0:2]) * 60 * 60 + int(progress_time[3:5]) * 60 + int(progress_time[6:8])
                self.progress = ('{0:.2f}').format(elapsed_time / total_dur * 100)
        
        if self.download.returncode == 0:
            self.progress = 100
            self.state = 'Complete'
        else:
            self.progress = "Error in downloading: {}\r".format(line)
            self.state = 'Error'
