class TestHistoryBuilder:
    def __init__(self):
        self.options = {}
    def withLimit(self, limit):
        self.options['num'] = limit
        return self
    def withActive(self, active):
        self.options['active'] = active
        return self
    def withName(self, name):
        self.options['name'] = name
        return self
    def withBuild(self, build):
        self.options['build ']= build
        return self
    def withUrl(self, url):
        self.options['url'] = url
        return self
    def withScore(self, score):
        self.options['score'] = score
        return self
    def withPlatform(self, platform):
        self.options['platform'] = platform
        return self
    def withPlatformType(self, platformType):
        self.options['platformType'] = platformType
        return self
    def withBrowser(self, browser):
        self.options['browser'] = browser
        return self
    def withBrowserType(self, browserType):
        self.options['browserType'] = browserType
        return self
    def withResolution(self, resolution):
        self.options['resolution']= resolution
        return self
    def withStartDate(self, startDate):
        self.options['startDate'] = startDate
        return self
    def withEndDate(self, endDate):
        self.options['endDate'] = endDate
        return self
    def build(self):
        return self.options
