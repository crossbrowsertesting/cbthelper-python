from . import globals as G
import requests, sys, time, os, threading

class Video:
    def __init__(self, hash, test):
        self.hash = hash
        self.testId = test.testId
        self.getInfo()
    def getInfo(self):
        self.info = requests.get(G.api + self.testId + '/videos/' + self.hash, auth=(G.username, G.authkey)).json()
        return self.info
    def stopRecording(self):
        requests.delete(G.api + self.testId + '/videos/' + self.hash, auth=(G.username, G.authkey))
    def setDescription(self, description):
        url = G.api + self.testId + '/videos/' + self.hash
        self.info = requests.put(url, auth=(G.username, G.authkey), data={'description':description})
    def saveLocally(self, location):
        t = threading.Thread(target=Video.__saveLocally, args=(self, location))
        t.start()
    def __saveLocally(self, location):
        self.getInfo()
        timeout = 20
        iteration = 1
        #while (iteration < timeout) and (self.info['is_finished'] == False):
        #    time.sleep(2)
        #    iteration += 1
        #    self.getInfo()
        if self.info['is_finished'] == False:
            self.stopRecording
        #iteration = 1
        url = self.info['video']
        r = requests.get(url, stream=True)
        while (iteration < timeout) and (r.status_code != 200):
            time.sleep(2)
            r = requests.get(url, stream=True)
            iteration += 1
        if iteration < timeout:
            with open(location, 'wb') as f:
                for chunk in r.iter_content(chunk_size=128):
                    f.write(chunk)
