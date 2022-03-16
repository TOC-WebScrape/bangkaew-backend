from src.util import EnvUtil
from src.binance import BinanceScript
import time


if __name__ == '__main__':
    # Delay 5 second to prevent preemptive establish connection to remote driver
    time.sleep(5)
    print("START SETUP SELENIUM")

    test = BinanceScript(
        url="https://www.binance.com/en/trade/BTC_USDT?layout=pro", pre_script_xpath_target=[
        ], actual_script_xpath_target=[], post_script_xpath_target=['/html/body/div[1]/div/div/div[2]/div/div[1]'])
    test.new_tab(url="https://www.binance.com/en/trade/ACA_USDT?layout=pro")
    test.new_tab(url="https://www.binance.com/en/trade/ADX_USDT?layout=pro")
    test.scrape_all_tab()
    test.tear_down()

    print("FINISH SETUP SELENIUM")
