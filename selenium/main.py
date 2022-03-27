from src.coingecko import CoingeckoScript
import time

if __name__ == '__main__':
    # Delay 5 second to prevent preemptive establish connection to remote driver
    time.sleep(5)
    print("START SETUP SELENIUM")

    coingecko = CoingeckoScript(name='coingecko', url='https://www.coingecko.com/en/coins/bitcoin#markets',
                                pre_script_xpath_target=[], actual_script_xpath_target=['/html/body/div[5]/div[7]/div[2]/div/div[1]/div/div[1]/div[3]/a'], post_script_xpath_target=['/html/body/div[5]/div[7]/div[2]/div/div[1]/div/div[1]/div[2]/table/tbody[2]'])

    print("FINISH SETUP SELENIUM")
