import requests
import re

START_DIV_CSS_NAME = 'css-1vuj9rf'

page_html = requests.get('https://www.binance.com/en/markets').text
reqex_result = re.search(START_DIV_CSS_NAME, page_html)
start_ind = reqex_result.start()

# print(start_ind)
# print(page_html[start_ind:start_ind+200:])

page_html = page_html[start_ind::]
