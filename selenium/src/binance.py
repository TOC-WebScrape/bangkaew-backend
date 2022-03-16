from .script_template import ScriptTemplate
from url_parser import get_url


class BinanceScript(ScriptTemplate):
    def __init__(self, url, pre_script_xpath_target, actual_script_xpath_target, post_script_xpath_target):
        super().__init__(url=url, pre_script_xpath_target=pre_script_xpath_target,
                         actual_script_xpath_target=actual_script_xpath_target, post_script_xpath_target=post_script_xpath_target)

    def post_script(self, xpath_target, name):

        # Extract raw HTML
        raw_data = self.get_element(xpath_target[0])
        self.write_to_txt(text=raw_data.get_attribute(
            "innerHTML"), name=name)

    def format_name(self, index):
        this_coin_url = self.get_list_tab()[index]
        domain_name = this_coin_url.replace("https://www.", "")
        domain_name = domain_name.replace(".com/en/trade", "")
        domain_name = domain_name.replace("_USDT?layout=pro", "")
        return domain_name
