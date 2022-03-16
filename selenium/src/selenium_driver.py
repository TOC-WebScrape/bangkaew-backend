from cmath import exp
import os
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys


class SeleniumDriver():
    _browser = None  # Instance driver
    _screenshot_path = "./screenshots/"  # Directory for screenshot
    _result_path = "./results/"  # Directory for raw data
    _screen_shot = True  # Default screenshot option
    _delay = 10  # Default delay

    _current_tab_index = 0  # Start at 0 (First tab)
    _total_number_of_tab = 0  # Start at 1
    _list_tab = []  # List of URL that are currently open

    def __init__(self, url):
        self._browser = self.set_up(url)

    def print_status(self):
        listToStr = ','.join([str(elem) for elem in self.get_list_tab()])
        print(listToStr + " | Total number of tab right now: " + str(self.get_total_number_of_tab()
                                                                     ) + ", Now you are at tab index: " + str(self.get_current_tab_index()))

    def get_current_tab_index(self):
        return self._current_tab_index

    def get_total_number_of_tab(self):
        return self._total_number_of_tab

    def get_list_tab(self):
        return self._list_tab

    def get_browser(self):
        return self._browser

    def add_list_tab(self, url):
        self._list_tab.append(url)
        self._total_number_of_tab = self._total_number_of_tab + 1

    def remove_list_tab(self, index):
        self._list_tab.pop(index)
        self._total_number_of_tab = self._total_number_of_tab - 1

    def toggle_screen_shot(self):
        self._screen_shot = not self._screen_shot

    def change_current_tab_index(self, new_index):
        self._current_tab_index = new_index

    def set_up(self, url):
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
        browser.get(url)
        self.add_list_tab(url=url)
        self.print_status()
        return browser

    def new_tab(self, url):
        try:
            self._browser.switch_to.new_window('tab')
            WebDriverWait(self._browser, self._delay
                          ).until(EC.number_of_windows_to_be(self.get_total_number_of_tab() + 1))
            self.add_list_tab(url=url)
            self.change_current_tab_index(self.get_total_number_of_tab() - 1)
            self.get_browser().get(url)
            self.print_status()
        except:
            print("Fail to open new tab to: " + url)

    def switch_to_tab_index(self, index):
        try:
            self.get_browser().switch_to.window(
                self.get_browser().window_handles[index])
            self.change_current_tab_index(index)
            self.print_status()
        except:
            print("Fail to switch to tab index " + str(index))

    def close_tab_and_switch_to_tab_index(self, index):
        try:
            if self.get_total_number_of_tab() == 1:
                self.tear_down()
                print("Tear down broswer because close the last tab")
            else:
                self.remove_list_tab(index=self.get_current_tab_index())
                self.get_browser().close()
                self.switch_to_tab_index(index)
        except:
            print("Fail to close tab and switch to tab index " + str(index))

    def tear_down(self):  # To shut down browser
        self.get_browser().quit()

    def get_element(self, xpath):  # Get element by XPATH
        target_element = WebDriverWait(self.get_browser(), self._delay).until(
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
        def S(X): return self.get_browser().execute_script(
            'return document.body.parentNode.scroll'+X)
        self.get_browser().set_window_size(S('Width'), S('Height'))

    # Take screenshot of entire body html
    def fullpage_screenshot(self, name):
        if(self._screen_shot):
            self.set_window_size_all_the_way()
            self.get_browser().find_element_by_tag_name(
                'body').screenshot(self._screenshot_path + name + ".png")

    # Wait element to load and click by XPATH
    def wait_to_load_and_click(self, xpath):
        try:
            WebDriverWait(self.get_browser(), self._delay).until(EC.element_to_be_clickable(
                (By.XPATH, xpath))).click()
        except:
            print("Unable to click element: " + xpath)

    # Export text to .txt in a single line
    def write_to_txt(self, text, name):
        try:
            save_path = self._result_path + name + '.txt'
            new_text = ''.join([line.strip() for line in text])
            with open(save_path, 'w') as f:
                f.write(new_text)
        except:
            print("Fail to write to txt: " + save_path)
