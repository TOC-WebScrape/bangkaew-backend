from src.selenium_driver import SeleniumDriver
import time

if __name__ == '__main__':
    time.sleep(3)  # Sleep for 3 seconds
    print("START SETUP SELENIUM")
    chrome_driver = SeleniumDriver(
        screenshot_path="./screenshots/", result_path="./results/")
    chrome = chrome_driver.browser

    chrome.get("https://selenium.dev")
    chrome_driver.fullpage_screenshot("test1.png")

    chrome_driver.tear_down()
    print("FINISH SETUP SELENIUM")
