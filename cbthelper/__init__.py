import requests

from . import globals as G
from .CapsBuilder import CapsBuilder
from .TestHistoryBuilder import TestHistoryBuilder
from .AutomatedTest import AutomatedTest
from .Snapshot import Snapshot

SCORE_PASS = 'pass'
SCORE_FAIL = 'fail'
SCORE_UNSET = 'unset'
hub = "http://hub.crossbrowsertesting.com:80/wd/hub"

def getCapsBuilder():
    G.capsBuilder = G.capsBuilder or CapsBuilder()
    return G.capsBuilder

def login(username, authkey):
    G.username = username
    G.authkey = authkey

def getTestHistoryBuilder():
    return TestHistoryBuilder()

def getTestHistory(options):
    return requests.get(G.api, auth=(G.username, G.authkey), data=options).json()
