from src.see_more_script import SeeMoreScript
import time

if __name__ == '__main__':
    time.sleep(5)
    print("START SETUP SELENIUM")

    coingecko = SeeMoreScript(url='https://www.coingecko.com/en/coins/bitcoin#markets',
                              pre_script_xpath_target=[], actual_script_xpath_target=['/html/body/div[5]/div[7]/div[2]/div/div[1]/div/div[1]/div[3]/a'])

    coingecko.tear_down()
    print("FINISH SETUP SELENIUM")
