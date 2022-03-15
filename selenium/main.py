from src.selenium_driver import SeleniumDriver
from src.see_more_script import SeeMoreScript
import time

if __name__ == '__main__':
    time.sleep(7)  # Sleep for 7 seconds
    print("START SETUP SELENIUM")

    coingecko = SeeMoreScript(url="https://www.coingecko.com/en/coins/bitcoin",
                              pre_script_xpath_target='/html/body/div[5]/div[7]/div[1]/div/div[1]/div[1]/div[4]/div/div[2]/a/span', actual_script_xpath_target='/html/body/div[5]/div[7]/div[2]/div/div[1]/div/div[1]/div[3]/a')

    coingecko.tear_down()
    print("FINISH SETUP SELENIUM")
