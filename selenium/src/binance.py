from .script_template import ScriptTemplate
import time


class BinanceScript(ScriptTemplate):
    def __init__(self, name, url, pre_script_xpath_target, actual_script_xpath_target, post_script_xpath_target):
        super().__init__(name)

        # Navigate to target webpage
        self._browser.get(url)
        # For waiting the web page to load in order to find out the final view size
        time.sleep(5)
        self.set_window_size_all_the_way()

        self.execute_script(pre_script_xpath_target,
                            actual_script_xpath_target, post_script_xpath_target)

    def post_script(self, xpath_target):
        # Screenshot for debug
        self.fullpage_screenshot(self.name + "_final.png")
        # Extract raw HTML
        raw_data = self.get_element(xpath_target[0])
        self.write_to_txt(text=raw_data.get_attribute(
            "innerHTML"), name="binance")
        # Shutdown browser
        self.tear_down()
