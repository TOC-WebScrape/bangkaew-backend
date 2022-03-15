import os
import time
from selenium import webdriver


class SeleniumDriver():
    browser = None
    screenshot_path = ""
    result_path = ""

    def __init__(self, screenshot_path, result_path):
        self.browser = self.set_up()
        self.screenshot_path = screenshot_path
        self.result_path = result_path

    def set_up(self):
        # Specifying argument as you launch your browser
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--incognito')
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument('--ignore-certificate-errors')
        chrome_options.add_argument('--start-maximized')

        # Create new Instance of Chrome
        browser = webdriver.Remote(
            os.getenv('REMOTE_SELENIUM_URL', 'http://selenium:4444'), options=chrome_options)
        browser.implicitly_wait(10)
        return browser

    def tear_down(self):
        self.browser.quit()

    def fullpage_screenshot(self, name):
        def S(X): return self.browser.execute_script(
            'return document.body.parentNode.scroll'+X)
        self.browser.set_window_size(S('Width'), S('Height'))
        self.browser.find_element_by_tag_name(
            'body').screenshot(self.screenshot_path+name)
