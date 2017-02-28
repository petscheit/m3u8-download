import sys, os, urllib.request

# M3U8 class with everything that is needed for parsing and downloading....
class LinkScrape:
    def __init__(self, indexLink, name):
        # initial constructor
        self.FilesLinks = []
        self.Link = indexLink
        self.Name = name

    def parse(self):
        # parse through file, checking for links
        try :
            lines = urllib.request.urlopen(self.Link).readlines()
            # Check for valid file format
            if lines[0].decode('utf-8').startswith('#EXTM3U'):
                for line in lines:
                    line=line.decode('utf-8').strip()
                    if not line.startswith('#'):
                        self.FilesLinks.append(line)
            else:
                print("File not valid!")
        except urllib.error.URLError as e:
            print("Link " + e.reason)

    def download(self):
        self.checkdir()
        # Iterates through array of parsed links
        for downloadLink in self.FilesLinks:
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
        if not os.path.exists(self.Name):
            os.makedirs(self.Name)
            return

    def createfilename(self, link):
        # creates filename including local dir based on url
        return self.Name + '/' + self.Name + '_' + link.split('/')[-1].split('?')[0]


