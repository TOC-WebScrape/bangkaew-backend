from .selenium_driver import SeleniumDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By


class SeeMoreScript(SeleniumDriver):
    _target_url = ""

    def __init__(self, url):
        super().__init__()
        self._target_url = url
        self.pre_script()

    def pre_script(self):
        print("Pre Script")
        self._browser.get(self._target_url)
        print("Done go to Target Web")
        self.fullpage_screenshot("test101.png")
        WebDriverWait(self._browser, 10).until(EC.element_to_be_clickable(
            (By.XPATH, '//*[@data-text = "OK"]'))).click()
        self.fullpage_screenshot("test102.png")
