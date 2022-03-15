from .selenium_driver import SeleniumDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import time


class SeeMoreScript(SeleniumDriver):
    _target_url = ""

    def __init__(self, url, pre_script_xpath_target, actual_script_xpath_target):
        super().__init__()
        self._target_url = url
        self.pre_script(pre_script_xpath_target)
        self.actual_script(actual_script_xpath_target)

    def wait_to_load_and_click(self, xpath):
        try:
            WebDriverWait(self._browser, 10).until(EC.element_to_be_clickable(
                (By.XPATH, xpath))).click()
        except:
            print("Unable to click element: " + xpath)

    def pre_script(self, xpath_target):  # Navigate to desire page
        self._browser.get(self._target_url)
        time.sleep(5)
        self.fullpage_screenshot("test101.png")
        self.wait_to_load_and_click(xpath_target)
        time.sleep(5)
        self.fullpage_screenshot("test102.png")

    def actual_script(self, xpath_target):  # Actual loop scirpt
        self.wait_to_load_and_click(xpath_target)
        time.sleep(10)
        self.fullpage_screenshot("test103.png")
