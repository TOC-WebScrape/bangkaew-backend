from src.binance import BinanceScript
import time
from joblib import Parallel, delayed


def task_function(task):
    driver, url_tasks = task.values()
    test = driver(
        url=url_tasks["urls"].pop(), pre_script_xpath_target=url_tasks["pre_script"], actual_script_xpath_target=url_tasks["real_script"], post_script_xpath_target=url_tasks["post_script"])

    for url in url_tasks["urls"]:
        test.new_tab(
            url=url)
    test.scrape_all_tab()
    test.tear_down()


if __name__ == '__main__':
    # Delay 5 second to prevent preemptive establish connection to remote driver
    time.sleep(5)
    print("START SETUP SELENIUM")

    tasks = [
        {
            "driver": BinanceScript,
            "url_tasks": {
                "pre_script": [],
                "real_script": [],
                "post_script": [
                    '/html/body/div[1]/div/div/div[2]/div/div[1]'
                ],
                "urls": [
                    "https://www.binance.com/en/trade/BTC_USDT?layout=pro",
                    "https://www.binance.com/en/trade/ACA_USDT?layout=pro",
                    "https://www.binance.com/en/trade/ADX_USDT?layout=pro"
                ],
            }
        }
    ]

    Parallel(n_jobs=-1)(delayed(task_function)(task) for task in tasks)

    print("FINISH SETUP SELENIUM")
