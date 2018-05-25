import cbthelper as cbt
from selenium import webdriver

def main():
    # set username and auth key for api requests
    username = ''
    authkey = ''
    cbt.login(username, authkey)
    # build caps using best match of what customer wants
    # does not require exact platform or browser name
    caps = cbt.getCapsBuilder() \
        .withPlatform('windows 10') \
        .withBrowser('Chrome 65') \
        .withResolution(1024, 768) \
        .withName('cbthelper test') \
        .withBuild('0.0.1') \
        .build()

    driver = webdriver.Remote(desired_capabilities = caps, command_executor = cbt.hub)
    driver.implicitly_wait(20)

    # initialize an AutomatedTest object with our selenium session id
    myTest = cbt.AutomatedTest(driver.session_id)

    driver.get('http://google.com')
    driver.implicitly_wait(2)
    # easily take snapshot
    googleSnap = myTest.takeSnapshot()
    # easily set snapshot description
    googleSnap.setDescription('google.com')
    # save the snapshot locally
    googleSnap.saveSnapshot('google.png')

    driver.get('http://crossbrowsertesting.com')
    driver.implicitly_wait(2)
    # take snapshot and set description with one call (that's all)
    myTest.takeSnapshot('cbt.com')

    # downloads every snapshot for a given test and saves them in a directory
    # can set useDescription to name the images what we set as the description
    # alternatively can set a prefix (default 'image') and images will be indexed
    myTest.saveAllSnapshots('./images', useDescription=True)

    # set score using enum (SCORE_PASS, _FAIL, or _UNSET)
    myTest.setScore(cbt.SCORE_PASS)

    # set description
    myTest.setDescription('blah blah blah')

    # send request to our api to stop the test
    # can also pass in score to set score and stop in one call
    # myTest.stop(cbt.SCORE_PASS)
    myTest.stop()

    #driver.quit()

    # our test history api call takes a lot of optional parameters
    # the builder makes it easier to get what you want
    options = cbt.getTestHistoryBuilder() \
        .withLimit(5) \
        .withName('cbthelper test') \
        .build()
    print(options)
    # grab our history using the options we created above
    history = cbt.getTestHistory(options)
    print(len(history['selenium']))

if __name__ == '__main__':
    main()
