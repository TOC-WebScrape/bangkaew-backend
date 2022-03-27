from .selenium_driver import SeleniumDriver


class SeeMoreScript(SeleniumDriver):
    _loop = 10  # Number of loop for actual script
    name = "no_name"  # Name of this target for save resource path

    def __init__(self, name):
        super().__init__()
        self.name = name

    def set_loop(self, new_loop):
        self._loop = new_loop

    def pre_script(self):  # Pre-scirpt
        return

    def actual_script(self):  # Actual loop scirpt
        return

    def post_script(self):  # Post-scirpt
        return
