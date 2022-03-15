from src.selenium_driver import SeleniumDriver
from src.see_more_script import SeeMoreScript
import time

if __name__ == '__main__':
    time.sleep(7)  # Sleep for 5 seconds
    print("START SETUP SELENIUM")

    coingecko = SeeMoreScript("https://www.coingecko.com/en/coins/bitcoin")

    coingecko.tear_down()
    print("FINISH SETUP SELENIUM")
