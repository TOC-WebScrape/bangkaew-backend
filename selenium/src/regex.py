import requests
import re

COIN_DIV_CLASS_NAME = '((<div direction=\"ltr\".*?)Trade+)'
COIN_DATA_DEVIDER = '<div data-area="'

page_html = open('dummy.txt', 'r').read()

coins_data = re.match(COIN_DIV_CLASS_NAME, page_html)
print(coins_data)
