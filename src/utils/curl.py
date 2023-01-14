import subprocess

# sampl_ command_of_mp4upload.com = 'curl.exe "https://www14.mp4upload.com:282/d/qwx22nozz3b4quuobkqbwz2ckrbhifhv2famtfhujlcnp76cdc7d7iwd/[SubsPlease]%20Tate%20no%20Yuusha%20no%20Nariagari%20S2%20-%2008%20(1080p)%20[1B2526A8].1080.mp4" --globoff -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:101.0) Gecko/20100101 Firefox/101.0" -H "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8" -H "Referer: https://www.mp4upload.com/" -H "Cookie: aff=421381; lang=english" -o curldown.mp4'

headers = '" --globoff -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:101.0) Gecko/20100101 Firefox/101.0" -H "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8" -H "Referer: https://www.mp4upload.com/"'

class curl_downloader:
    def __init__(self, epi_url, title, dir_name, *args):
        self.cmd = 'curl.exe "' + epi_url + headers + " -o " + title + '.mp4'
        self.directory = dir_name
        self.title = title
        self.line = ''
        self.progress = 0
        self.size = 0
        self.elapsed_time = 0
        self.duration = 0
        self.state = None  # gives current condition of download
        self.speed = '0'


        self.line = ''
        self.progress = 0
        self.size = 0
        self.elapsed_time = 0

    def to_bytes(size: str):
        if size.endswith('M'):
            return float(size[:-1:])*1024*1024
        elif size.endswith('k'):
            return float(size[:-1:])*1024
        else:
            return float(size[:-1:])

    def make_command(url: str, name: str):
        return 'curl.exe "' + url + '" --globoff -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:101.0) Gecko/20100101 Firefox/101.0" -H "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8" -H "Referer: https://www.mp4upload.com/" -o ' + name

    def start_download(self):
        self.download = subprocess.Popen(
            self.cmd,
            universal_newlines=False, 
            stderr=subprocess.STDOUT, 
            stdout=subprocess.PIPE, 
            stdin=subprocess.PIPE,
        )

    def track(self):

        while True:
            if self.download.stdout is None:
                continue
            self.line = self.download.stdout.readline().decode("utf-8").strip()
            if self.line == "" and self.download.poll() is not None:
                break
            if self.line.endswith('Speed'):
                break

        self.state = 'Downloading'
        while True:
            if self.download.stdout is None:
                continue
            self.line = self.download.stdout.read(79).decode("utf-8") # this 79 is trial and error guess dont know how and why this is working. Have to find an alternative.
            if self.line == "" and self.download.poll() is not None:
                break
            else:
                spl_line = line.split()
                if spl_line[1] != '0':
                    total_size = self.to_bytes(spl_line[1])
                    break

        while True:
            if self.download.stdout is None:
                continue
            self.line = self.download.stdout.read(79).decode("utf-8") # this 79 is a trial and error guess dont know who and why this is working. Have to find an altenative
            if line == "" and self.download.poll() is not None:
                break
            else:
                line = line.split()
                self.progress = self.to_bytes(line[3])*100/total_size
                self.speed = line[-1]
        
            if line[1] == line[3]:
                self.state = "\nDownload Complete"