import os
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException


class SeleniumDriver():
    _browser = None
    _screenshot_path = "./screenshots/"
    _result_path = "./results/"
    _screen_shot = True
    _delay = 10

    def __init__(self):
        self._browser = self.set_up()

    def get_browser(self):
        return self._browser

    def toggle_screen_shot(self):
        self._screen_shot = not self._screen_shot

    def set_up(self):
        # Specifying argument as you launch your browser
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--incognito')
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument('--ignore-certificate-errors')
        chrome_options.add_argument('--start-maximized')
        # ! Pevent "unknown error: session deleted because of page, Take out once on production, see ref at: https://stackoverflow.com/questions/53902507/unknown-error-session-deleted-because-of-page-crash-from-unknown-error-cannot
        chrome_options.add_argument('--disable-dev-shm-usage')

        # Create new Instance of Chrome
        browser = webdriver.Remote(
            os.getenv('REMOTE_SELENIUM_URL', 'http://selenium:4444'), options=chrome_options)
        return browser

    def tear_down(self):
        self._browser.quit()

    def wait_element_to_load(self, xpath):
        try:
            WebDriverWait(self.
                          _browser, self._delay).until(EC.presence_of_element_located((By.XPATH, xpath)))
            print("Element is ready!")
        except TimeoutException:
            print("Element: " + xpath + " loading took too much time!")

    def set_window_size_all_the_way(self):
        def S(X): return self._browser.execute_script(
            'return document.body.parentNode.scroll'+X)
        self._browser.set_window_size(S('Width'), S('Height'))

    def fullpage_screenshot(self, name):
        if(self._screen_shot):
            self.set_window_size_all_the_way()
            self._browser.find_element_by_tag_name(
                'body').screenshot(self._screenshot_path+name)

    def wait_to_load_and_click(self, xpath):
        try:
            WebDriverWait(self._browser, self._delay).until(EC.element_to_be_clickable(
                (By.XPATH, xpath))).click()
        except:
            print("Unable to click element: " + xpath)
