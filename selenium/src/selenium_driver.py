import os
from selenium import webdriver


class SeleniumDriver():

    def __init__(self):
        # Specifying argument as you launch your browser
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--incognito')
        chrome_options.add_argument("--no-sandbox")

        # Create new Instance of Chrome
        browser = webdriver.Remote(
            os.getenv('REMOTE_SELENIUM_URL', 'http://selenium:4444'), options=chrome_options)
        self.driver = browser
        return self.driver
