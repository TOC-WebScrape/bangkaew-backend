from src.binance import BinanceScript
from src.gate import GateScript
from src.kucoin import KuCoinScript
from src.bitmart import BitMartScript
from joblib import Parallel, delayed
import time


def task_function(task):
    driver, url_tasks = task.values()
    browser = driver(
        url=url_tasks["urls"].pop(), pre_script_xpath_target=url_tasks["pre_script"], actual_script_xpath_target=url_tasks["real_script"], post_script_xpath_target=url_tasks["post_script"])

    for url in url_tasks["urls"]:
        browser.new_tab(
            url=url)
    browser.scrape_all_tab()
    browser.tear_down()


if __name__ == '__main__':
    # Delay 5 second to prevent preemptive establish connection to remote driver
    time.sleep(5)
    print("START SELENIUM")

    tasks = [
        {
            "driver": BinanceScript,
            "url_tasks": {
                "pre_script": ['/html/body/div[1]/div/div/main/div/div[2]/div/div/div[2]/div[3]/div/button[%]'],
                "real_script": [],
                "post_script": [
                    '/html/body/div[1]/div/div/main/div/div[2]/div/div/div[2]/div[2]/div/div[2]'
                ],
                "urls": [
                    "https://www.binance.com/en/markets/spot-USDT",
                    "https://www.binance.com/en/markets/spot-USDT",
                    "https://www.binance.com/en/markets/spot-USDT",
                    "https://www.binance.com/en/markets/spot-USDT",
                    "https://www.binance.com/en/markets/spot-USDT",
                    "https://www.binance.com/en/markets/spot-USDT",
                    "https://www.binance.com/en/markets/spot-USDT",
                ],
            }
        },
        # {
        #     "driver": GateScript,
        #     "url_tasks": {
        #         "pre_script": ['/html/body/div[1]/div[1]/div/div/div[2]/div[2]/div/button[3]/em'],
        #         "real_script": [],
        #         "post_script": [
        #             '/html/body/div[1]/div[1]/div/div/div[3]/div/div/table/tbody'
        #         ],
        #         "urls": [
        #             "https://www.gate.io/th/marketlist?tab=usdt",
        #         ],
        #     }
        # },
        # {
        #     "driver": KuCoinScript,
        #     "url_tasks": {
        #         "pre_script": ['/html/body/div[1]/div/div/div[3]/div/div[3]/div/div/div/div[1]/div[1]/div[1]/div/div[3]/div/button[2]/span[1]/div/span', '/html/body/div[1]/div/div/div[3]/div/div[3]/div/div/div/div[1]/div[2]/div[1]/div/div[2]'],
        #         "real_script": [],
        #         "post_script": [
        #             '/html/body/div[1]/div/div/div[3]/div/div[3]/div/div/div/div[3]/div/div[1]/div[2]/div/div/div/div/div/div/div/div/table/tbody'
        #         ],
        #         "urls": [
        #             "https://www.kucoin.com/markets?spm=kcWeb.B1homepage.Header3.1",
        #         ],
        #     }
        # },
        # {
        #     "driver": BitMartScript,
        #     "url_tasks": {
        #         "pre_script": ['/html/body/div[1]/div/div/div[2]/div[2]/div[2]/div[1]/div[3]/div[1]/div[2]/div[1]/div/div/div/div[3]'],
        #         "real_script": [],
        #         "post_script": [
        #             '/html/body/div[1]/div/div/div[2]/div[2]/div[2]/div[1]/div[3]/div[1]/div[2]/div[2]/div[2]/div/ul'
        #         ],
        #         "urls": [
        #             "https://www.bitmart.com/markets/en?markettype=spot",
        #         ],
        #     }
        # }
    ]

    Parallel(n_jobs=-1)(delayed(task_function)(task) for task in tasks)

    print("FINISH SELENIUM")
