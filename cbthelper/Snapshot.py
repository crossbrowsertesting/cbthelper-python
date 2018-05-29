from . import globals as G
import requests, sys, time, os, threading

class Snapshot:
    def __init__(self, hash, test):
        self.hash = hash
        self.testId = test.testId
        self.getInfo()
    def getInfo(self):
        self.info = requests.get(G.api + self.testId + '/snapshots/' + self.hash, auth=(G.username, G.authkey)).json()
        return self.info
    def setDescription(self, description):
        url = G.api + self.testId + '/snapshots/' + self.hash
        self.info = requests.put(url, auth=(G.username, G.authkey), data={'description':description})
    def saveLocally(self, location):
        t = threading.Thread(target=Snapshot.__saveSnapshot, args=(self, location))
        t.start()
    def __saveSnapshot(self, location):
        url = self.getInfo()['image']
        r = requests.get(url, stream=True)
        timeout = 15
        iteration = 1
        while (iteration < timeout) and (r.status_code != 200):
            r = requests.get(url, stream=True)
            iteration += 1
            time.sleep(1)
        if iteration < timeout:
            with open(location, 'wb') as f:
                for chunk in r.iter_content(chunk_size=128):
                    f.write(chunk)
