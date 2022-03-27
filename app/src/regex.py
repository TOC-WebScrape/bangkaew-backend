import requests
import re

START_DIV_CSS_NAME = 'css-1vuj9rf'
COIN_DIV_CLASS_NAME = 'css-vlibs4'

page_html = requests.get('https://www.binance.com/en/markets').text
regex_result = re.search(START_DIV_CSS_NAME, page_html)
start_ind = regex_result.start()
page_html = page_html[start_ind::]

regex_result = re.findall(COIN_DIV_CLASS_NAME, page_html)
print(len(regex_result))
