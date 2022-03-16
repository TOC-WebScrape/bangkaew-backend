from .selenium_driver import SeleniumDriver


class ScriptTemplate(SeleniumDriver):
    _loop = 10  # Number of loop for actual script
    name = "no_name"  # Name of this target for save resource path

    def __init__(self, name):
        super().__init__()
        self.name = name

    def set_loop(self, new_loop):
        self._loop = new_loop

    def execute_script(self, pre_script_xpath_target, actual_script_xpath_target, post_script_xpath_target):
        if pre_script_xpath_target:
            self.pre_script(pre_script_xpath_target)
        if actual_script_xpath_target:
            self.actual_script(actual_script_xpath_target)
        if post_script_xpath_target:
            self.post_script(post_script_xpath_target)

    def pre_script(self):  # Pre-scirpt
        return

    def actual_script(self):  # Actual loop scirpt
        return

    def post_script(self):  # Post-scirpt
        return
