from .selenium_driver import SeleniumDriver


class ScriptTemplate(SeleniumDriver):
    pre_script_xpath_target = []
    actual_script_xpath_target = []
    post_script_xpath_target = []

    def __init__(self, url, pre_script_xpath_target, actual_script_xpath_target, post_script_xpath_target):
        super().__init__(url=url)
        self.pre_script_xpath_target = pre_script_xpath_target
        self.actual_script_xpath_target = actual_script_xpath_target
        self.post_script_xpath_target = post_script_xpath_target

    def scrape_all_tab(self):
        for x in range(self.get_total_number_of_tab()):
            domain_name = self.format_name(x)
            self.switch_to_tab_index(x)
            self.fullpage_screenshot(name=domain_name)
            self.execute_script(domain_name)

    def valid(self):
        return  # TODO Find out if target URL is real

    def execute_script(self, name):
        if self.pre_script_xpath_target:
            self.pre_script(self.pre_script_xpath_target)
        if self.actual_script_xpath_target:
            self.actual_script(self.actual_script_xpath_target)
        if self.post_script_xpath_target:
            self.post_script(self.post_script_xpath_target,
                             name)

    def pre_script(self):  # Pre-scirpt
        return

    def actual_script(self):  # Actual loop scirpt
        return

    def post_script(self):  # Post-scirpt
        return

    def format_name(self, url):
        return
