import json
import os
from src.selenium_driver import SeleniumDriver
from src.util import EnvUtil
from src.binance import BinanceScript
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from joblib import Parallel, delayed


def take_screenshot(url):
    # Specifying argument as you launch your browser
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--incognito')
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--start-maximized')
    # ! Prevent "unknown error: session deleted because of page, Take out once on production, see ref at: https://stackoverflow.com/questions/53902507/unknown-error-session-deleted-because-of-page-crash-from-unknown-error-cannot
    # chrome_options.add_argument('--disable-dev-shm-usage')

    # Create new Instance of Chrome
    browser = webdriver.Remote(
        os.getenv('REMOTE_SELENIUM_URL', 'http://selenium:4444'), options=chrome_options)
    browser.get(url)
    file_name = url.split("//")[1]
    browser.get_screenshot_as_file(f"./screenshots/{file_name}.png")
    browser.quit()


if __name__ == '__main__':
    # Delay 5 second to prevent preemptive establish connection to remote driver
    time.sleep(10)
    print("START SETUP SELENIUM")
    # test = BinanceScript(
    #     url="https://www.binance.com/en/trade/BTC_USDT?layout=pro", pre_script_xpath_target=[
    #     ], actual_script_xpath_target=[], post_script_xpath_target=['/html/body/div[1]/div/div/div[2]/div/div[1]'])

    # for i in range(100):
    #     test.new_tab(
    #         url="https://www.binance.com/en/trade/ACA_USDT?layout=pro")
    #     test.new_tab(
    #         url="https://www.binance.com/en/trade/ADX_USDT?layout=pro")
    # test.scrape_all_tab()
    # test.tear_down()
    urls = [
        "https://www.google.com",
        "https://www.youtube.com",
        "https://anime-sugoi.com",
        "https://www.facebook.com"
    ]

    Parallel(n_jobs=-1)(delayed(take_screenshot)(url) for url in urls)

    print("FINISH SETUP SELENIUM")
