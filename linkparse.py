import sys, os, urllib.request, time
from threading import Thread

# M3U8 class with everything that is needed for parsing and downloading....
class Linkparse(Thread):
    def __init__(self, name, indexlink):
        # initial constructor
        Thread.__init__(self)
        self.fileslink = []
        self.link = indexlink
        self.name = name
        self.sleeptime = 0

    def run(self):
        while True:
            self.parse()
            self.download()
            time.sleep(self.sleeptime)
            self.sleeptime = 0
            self.fileslink = []

    def parse(self):
        # parse through file, checking for links
        try :
            lines = urllib.request.urlopen(self.link).readlines()
            # Check for valid file format
            if lines[0].decode('utf-8').startswith('#EXTM3U'):
                for line in lines:
                    line=line.decode('utf-8').strip()
                    if line.startswith('#EXTINF:'):
                        # reads sequene lenght from EXTINF
                        self.sleeptime += int(line.split(':')[1].split('.')[0]) * 0.95
                    if not line.startswith('#'):
                        self.fileslink.append(line)
            else:
                print("File not valid!")
        except urllib.error.URLError as e:
            print("Link " + e.reason)

    def download(self):
        self.checkdir()
        # Iterates through array of parsed links
        for downloadLink in self.fileslink:
            filename = self.createfilename(downloadLink)
            # Downloads video file
            if not os.path.exists(filename):
                try :
                    urllib.request.urlretrieve(downloadLink, filename)
                    print ("saved: " + filename)
                except urllib.error.URLError as e:
                    print("Link " + e.reason)
            else:
                print("skipping download")

    def checkdir(self):
        # checks if dir with name exists already and creates a new one if needed
        if not os.path.exists(self.name):
            os.makedirs(self.name)
            return

    def createfilename(self, link):
        # creates filename including local dir based on url
        return self.name + '/' + self.name + '_' + link.split('/')[-1].split('?')[0]

arte = Linkparse('arte', 'http://artelive-lh.akamaihd.net/i/artelive_de@393591/index_3_av-b.m3u8?sd=10&rebase=on')
arte.start()
