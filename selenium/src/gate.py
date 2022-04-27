import time
from .script_template import ScriptTemplate
from .custom_regex import extract_coin_data


class GateScript(ScriptTemplate):
    def __init__(self, url, pre_script_xpath_target, actual_script_xpath_target, post_script_xpath_target):
        super().__init__(url=url, pre_script_xpath_target=pre_script_xpath_target,
                         actual_script_xpath_target=actual_script_xpath_target, post_script_xpath_target=post_script_xpath_target)

    def post_script(self, xpath_target, name):
        time.sleep(4)
        # Extract raw HTML
        raw_data = self.get_element(xpath_target[0])
        data_to_write = raw_data.get_attribute(
            "innerHTML")
        current_page_number = self.get_current_tab_index() + 1
        actual_name = name + str(current_page_number)
        self.write_to_txt(text=data_to_write, name=actual_name)
        output = extract_coin_data(data=data_to_write, option='g')
        output.to_csv('./data/g.csv', index=False)

    def format_name(self, index):
        url = self.get_list_tab()[index]
        domain_name = url.replace("https://www.", "")
        domain_name = domain_name.replace(".io/th/marketlist?tab=usdt", "")
        return domain_name
