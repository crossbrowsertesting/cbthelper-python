from fuzzywuzzy import fuzz
from . import globals as G
import requests

class CapsBuilder:
    capsData = None
    def __init__(self):
        if not CapsBuilder.capsData:
            CapsBuilder.capsData = requests.get(G.api + 'browsers').json()
        self.platform = None
        self.browser = None
        self.width = None
        self.height = None
        self.name = None
        self.version = None
        self.recordVideo = None
        self.recordNetwork = None
    def withPlatform(self, platform):
        self.platform = platform
        return self
    def withBrowser(self, browser):
        self.browser = browser
        return self
    def withResolution(self, width, height):
        self.width = width
        self.height = height
        return self
    def withName(self, name):
        self.name = name
        return self
    def withBuild(self, build):
        # cant be build because of method below
        self.version = build
        return self
    def withRecordVideo(self, bool):
        self.recordVideo = bool
        return self
    def withRecordNetwork(self, bool):
        self.recordNetwork = bool
        return self
    def build(self):
        return self.__choose()
    def __bestOption(self, options, target):
        bestRatio = 0
        bestOption = None
        target = target.lower()
        target = target.replace('x64', '64-bit')
        for option in options:
            name = option['name'].lower()
            apiName = option['api_name'].lower()
            ratio = fuzz.partial_ratio(name, target)
            ratio += fuzz.partial_ratio(apiName, target)
            ratio += fuzz.ratio(name, target)
            ratio += fuzz.ratio(apiName, target)
            if ratio > bestRatio:
                bestRatio = ratio
                bestOption = option
        return bestOption
    def __bestBrowserNoPlatform(self, target):
        bestRatio = 0
        bestOption = None
        target = target.lower()
        target = target.replace('x64','64-bit')
        for platform in CapsBuilder.capsData:
            for browser in platform['browsers']:
                name = browser['name'].lower()
                apiName = browser['api_name'].lower()
                ratio = fuzz.partial_ratio(name, target)
                ratio += fuzz.partial_ratio(apiName, target)
                ratio += fuzz.ratio(name, target)
                ratio += fuzz.ratio(apiName, target)
                if ratio > bestRatio:
                    bestRatio = ratio
                    bestOption = browser
        return bestOption
    def __choose(self):
        data = CapsBuilder.capsData
        caps = {
            'username': G.username,
            'password': G.authkey
        }
        platform = None
        browser = None
        if self.platform:
            platform = self.__bestOption(data, self.platform)
            caps.update(platform['caps'])
        if self.browser:
            if platform:
                browser = self.__bestOption(platform['browsers'], self.browser)
            else:
                browser = self.__bestBrowserNoPlatform(self.browser)
            caps.update(browser['caps'])
        if self.width and self.height:
            caps['screenResolution'] = str(self.width) + 'x' + str(self.height)
        if self.name:
            caps['name'] = self.name
        if self.version:
            caps['build'] = self.version
        if self.recordVideo:
            caps['record_video'] = self.recordVideo
        if self.recordNetwork:
            caps['record_network'] = self.recordNetwork
        return caps
