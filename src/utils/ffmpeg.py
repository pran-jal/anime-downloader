import subprocess

class ffmpeg_downloader:        
    def __init__(self, down_link, title, dir_name, referer, *args):
        self.cmd = ['ffmpeg'] + [*args] + ['-referer', referer, '-i', down_link, '-c', 'copy', title + '.mp4', '-progress', '-']
        self.directory = dir_name
        self.title = title
        self.line = ''
        self.progress = 0
        self.size = 0
        self.elapsed_time = 0
        self.duration = 0
        self.state = None  # gives current condition of download
        self.speed = '0'
    
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
            self.line = self.download.stdout.readline().decode("utf-8").strip()
            if self.line == "" and self.download.poll() is not None:
                break
            if self.line.startswith('Duration: '):
                total_duration = self.line.split(', ')[0][10:]
                self.duration = int(total_duration[0:2]) * 60 * 60 + int(total_duration[3:5]) * 60 + int(total_duration[6:8])
                break
        
        while True:
            word = self.download.stdout.read(1).decode("utf-8")
            if word == "" and self.download.poll() is not None:
                break
            if word == '\n':
                self.line = ""
            else:
                self.line += word
            if self.line == f"File '{self.title}.mp4' already exists. Overwrite? [y/N] ":
                self.state = "waiting for overwrite conformation"
                self.download.stdin.write(bytes(input(self.line)+'\n', 'utf-8'))
                self.download.stdin.flush()
                break
            elif self.line.startswith('out_time='):      #this means that there is nothing to overwrite. i.e this is first download.
                break
        
        self.state = 'Downloading'
        while True:
            if self.download.stdout is None:
                continue
            self.line = self.download.stdout.readline().decode("utf-8").strip()
            if self.line == "" and self.download.poll() is not None:
                break 
            if self.line.startswith('out_time='):
                progress_time = self.line[9:]
                self.elapsed_time = int(progress_time[0:2]) * 60 * 60 + int(progress_time[3:5]) * 60 + int(progress_time[6:8])
                self.progress = ('{0:.2f}').format(self.elapsed_time / self.duration * 100)
        
        if self.download.returncode == 0:
            self.progress = 100
            self.state = 'Complete'
        else:
            self.progress = "Error in downloading: {}\r".format(self.line)
            self.state = 'Error'
