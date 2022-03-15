import os
from selenium import webdriver


class SeleniumDriver():
    _browser = None
    _screenshot_path = "./screenshots/"
    _result_path = "./results/"

    def __init__(self):
        self._browser = self.set_up()

    def get_browser(self):
        return self._browser

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
        self._browser.quit()

    def fullpage_screenshot(self, name):
        def S(X): return self._browser.execute_script(
            'return document.body.parentNode.scroll'+X)
        self._browser.set_window_size(S('Width'), S('Height'))
        self._browser.find_element_by_tag_name(
            'body').screenshot(self._screenshot_path+name)
