import os
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException


class SeleniumDriver():
    _browser = None  # Instance driver
    _screenshot_path = "./screenshots/"  # Directory for screenshot
    _result_path = "./results/"  # Directory for raw data
    _screen_shot = True  # Default screenshot option
    _delay = 10  # Default delay
    _keep_alive = True  # To keep observe
    _current_tab = []

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
        # ! Prevent "unknown error: session deleted because of page, Take out once on production, see ref at: https://stackoverflow.com/questions/53902507/unknown-error-session-deleted-because-of-page-crash-from-unknown-error-cannot
        chrome_options.add_argument('--disable-dev-shm-usage')

        # Create new Instance of Chrome
        browser = webdriver.Remote(
            os.getenv('REMOTE_SELENIUM_URL', 'http://selenium:4444'), options=chrome_options)
        return browser

    def tear_down(self):  # To shut down browser
        self._browser.quit()

    def get_element(self, xpath):  # Get element by XPATH
        target_element = WebDriverWait(self._browser, self._delay).until(
            EC.presence_of_element_located((By.XPATH, xpath)))
        return target_element

    def wait_element_to_load(self, xpath):  # Wait element to load by XPATH
        try:
            WebDriverWait(self.
                          _browser, self._delay).until(EC.presence_of_element_located((By.XPATH, xpath)))
        except TimeoutException:
            print("Element: " + xpath + " loading took too much time!")

    # Set window size to fit entire html element
    def set_window_size_all_the_way(self):
        def S(X): return self._browser.execute_script(
            'return document.body.parentNode.scroll'+X)
        self._browser.set_window_size(S('Width'), S('Height'))

    # Take screenshot of entire body html
    def fullpage_screenshot(self, name):
        if(self._screen_shot):
            self.set_window_size_all_the_way()
            self._browser.find_element_by_tag_name(
                'body').screenshot(self._screenshot_path+name)

    # Wait element to load and click by XPATH
    def wait_to_load_and_click(self, xpath):
        try:
            WebDriverWait(self._browser, self._delay).until(EC.element_to_be_clickable(
                (By.XPATH, xpath))).click()
        except:
            print("Unable to click element: " + xpath)

    # Export text to .txt in a single line
    def write_to_txt(self, text, name):
        new_text = ''.join([line.strip() for line in text])
        with open(self._result_path + name + '.txt', 'w') as f:
            f.write(new_text)
