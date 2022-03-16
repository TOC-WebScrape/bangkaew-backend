from src.util import EnvUtil
from src.binance import BinanceScript
import time


if __name__ == '__main__':
    # Delay 5 second to prevent preemptive establish connection to remote driver
    time.sleep(5)
    print("START SETUP SELENIUM")

    # binance = BinanceScript(name=EnvUtil.get_or_raise("BINANCE_NAME"), url=EnvUtil.get_or_raise("BINANCE_GENERAL_URL"), pre_script_xpath_target=[
    # ], actual_script_xpath_target=[], post_script_xpath_target=['/html/body/div[1]/div/div/div[4]/div/div[1]'])

    print("FINISH SETUP SELENIUM")
