import sys
import concurrent.futures
import subprocess
import os
import re

class Getframes():
  FFMPEG_PATH = '/usr/local/bin/ffmpeg'

  def __init__(self, dir, workers):
    # initial constructor
    self.q = []
    self.dir = dir
    self.workers = workers
    command = ['/usr/local/bin/ffmpeg', '-i', 'arte/arte_segment148830616_3_av-b.ts',  '-vf', 'fps=1', '-strftime', '1', "test_%02d.jpg"]
    subprocess.call(command)


  def main(self):
    self.queue()
    with concurrent.futures.ProcessPoolExecutor(self.workers) as executor:
        for video in self.q:
          print(video)
          executor.submit(self.renderframes, video)

  def queue(self):
    for file in os.listdir(self.dir):
      self.q.append(self.dir + '/' + file)

  @staticmethod
  def renderframes(video):
      print('arrived')
      name = re.findall(r'\d{9}', video)[0]
      print(video)
      command = [FFMPEG_PATH, '-i', video,  '-vf', 'fps=1', '-strftime', '1', "huhuhuhuhu_%02d.jpg"]
      subprocess.call(command)


render = Getframes('arte', 2)
render.main()

