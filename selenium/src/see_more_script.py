from .selenium_driver import SeleniumDriver
import time


class SeeMoreScript(SeleniumDriver):
    _loop = 10

    def __init__(self, url, pre_script_xpath_target, actual_script_xpath_target):
        super().__init__()

        self._browser.get(url)
        time.sleep(5)
        self.set_window_size_all_the_way()

        if pre_script_xpath_target:
            self.pre_script(pre_script_xpath_target)
        if actual_script_xpath_target:
            self.actual_script(actual_script_xpath_target)

    def set_loop(self, new_loop):
        self._loop = new_loop

    def pre_script(self, xpath_target):
        return

    def actual_script(self, xpath_target):  # Actual loop scirpt
        for x in range(self._loop):
            print(x)
            try:
                self.wait_element_to_load(xpath_target[0])
                self.wait_to_load_and_click(xpath_target[0])
            except:
                print("error")
                break
        time.sleep(3)
        self.fullpage_screenshot("coingecko_final.png")

        # def post_script(self):
