from gc import set_debug
import time
from .script_template import ScriptTemplate


class BitMartScript(ScriptTemplate):
    def __init__(self, url, pre_script_xpath_target, actual_script_xpath_target, post_script_xpath_target):
        super().__init__(url=url, pre_script_xpath_target=pre_script_xpath_target,
                         actual_script_xpath_target=actual_script_xpath_target, post_script_xpath_target=post_script_xpath_target)

    def pre_script(self, xpath_target):
        time.sleep(4)
        self.wait_to_load_and_click(xpath_target[0])

    def post_script(self, xpath_target, name):
        time.sleep(2)
        # Extract raw HTML
        raw_data = self.get_element(xpath_target[0])
        current_page_number = self.get_current_tab_index() + 1
        actual_name = name + str(current_page_number)
        self.write_to_txt(text=raw_data.get_attribute(
            "innerHTML"), name=actual_name)

    def format_name(self, index):
        url = self.get_list_tab()[index]
        domain_name = url.replace("https://www.", "")
        domain_name = domain_name.replace(
            ".com/markets/en?markettype=spot", "")
        return domain_name
