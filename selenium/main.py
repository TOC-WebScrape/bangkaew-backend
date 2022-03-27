from src.binance import BinanceScript
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
    print("START SETUP SELENIUM")

    tasks = [
        {
            "driver": BinanceScript,
            "url_tasks": {
                "pre_script": ['/html/body/div[1]/div/div/main/div/div[2]/div/div/div[2]/div[3]/div/button[%]'],
                "real_script": [],
                "post_script": [
                    '/html/body'
                ],
                "urls": [
                    "https://www.binance.com/en/markets",
                    "https://www.binance.com/en/markets",
                    "https://www.binance.com/en/markets",
                    "https://www.binance.com/en/markets",
                    "https://www.binance.com/en/markets",
                    "https://www.binance.com/en/markets",
                    "https://www.binance.com/en/markets",
                    "https://www.binance.com/en/markets",
                ],
            }
        },
        {
            "driver": BinanceScript,
            "url_tasks": {
                "pre_script": [],
                "real_script": [],
                "post_script": [
                    '/html/body'
                ],
                "urls": [
                    "https://www.gate.io/th/marketlist?tab=usdt",
                ],
            }
        }
    ]

    Parallel(n_jobs=-1)(delayed(task_function)(task) for task in tasks)

    print("FINISH SETUP SELENIUM")
