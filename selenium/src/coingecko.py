from .see_more_script import SeeMoreScript
import time


class CoingeckoScript(SeeMoreScript):
    def __init__(self, name, url, pre_script_xpath_target, actual_script_xpath_target, post_script_xpath_target):
        super().__init__(name)

        # Navigate to target webpage
        self._browser.get(url)
        # For waiting the web page to load in order to find out the final view size
        time.sleep(5)
        self.set_window_size_all_the_way()

        if pre_script_xpath_target:
            self.pre_script(pre_script_xpath_target)
        if actual_script_xpath_target:
            self.actual_script(actual_script_xpath_target)
        if post_script_xpath_target:
            self.post_script(post_script_xpath_target)

    def actual_script(self, xpath_target):
        # loop _loop times
        for x in range(self._loop):
            print(x)
            try:
                self.wait_to_load_and_click(
                    xpath_target[0])  # Click "See more"
            except:
                break
        # Delay for waiting page to load in order to screenshot
        time.sleep(3)
        # Screenshot for debug
        self.fullpage_screenshot(self.name + "_final.png")

    def post_script(self, xpath_target):
        # Extract raw HTML
        raw_data = self.get_element(xpath_target[0])
        self.write_to_txt(raw_data.get_attribute("innerHTML"))
        # Shutdown browser
        self.tear_down()
