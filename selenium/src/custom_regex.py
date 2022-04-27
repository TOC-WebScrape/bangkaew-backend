from distutils.log import error
import re
import pandas as pd
import sys

COIN_DIV_CLASS_NAME = ''
COIN_DATA_EXTRACT = ''
# <div.*?>(.*?)<\/div> # เอาข้อมูล child ออกมา
# >(.*?)< # อันนี้สั้นกว่าข้อมูลครบเหมือนกันได้ช่วงที่ต้องการมาเลย

# ฟังก์ชั่นนี้รับข้อมูลเป็น str ส่วนของ table และทำการใช้ regex นำข้อมูลออกมา และส่งกลับคืนเป็น python dict
# โดยมี key ดังนี้
# "short_name" คือ ชื่อย่อของเหรียญ
# "full_name" คือ ชื่อเต็มของเหรียญ
# "price" คือ ราคาปัจจุบัน
# "change" คือ การเปลี่ยนแปลงของราคาในช่วง 24 ชม
# "volume" คือ volume ในช่วง 24 ชม
# "market_cap" คือ market_cap

# และในการเข้าถึงข้อมูลสามารถทำได้โดยใช้ค่า index เนื่องจากตั้งให้ key ตรงกับเลข index เพื่อความง่ายในการใช้งาน

# ในการใช้งานไฟล์สามารถดูได้จากไฟล์ custom_regex_example.py ได้


def extract_coin_data(data, option):

    try:
        if option == 'bn':
            print("\n\nBINANCE")
            COIN_DIV_CLASS_NAME = '((<div direction=\"ltr\".*?)Trade)'
            coins_data_list = re.findall(COIN_DIV_CLASS_NAME, data)
            coin_data = extract_binance_coin_data(coins_data_list)
        elif option == 'bm':
            print("\n\nBITMART")
            COIN_DIV_CLASS_NAME = '(<tr .*?<\/tr>)'
            coins_data_list = re.findall(COIN_DIV_CLASS_NAME, data)
            coin_data = extract_bitmart_coin_data(coins_data_list)
        elif option == 'g':
            print("\n\nGATE")
            COIN_DIV_CLASS_NAME = '(<tr .*?<\/tr>)'
            coins_data_list = re.findall(COIN_DIV_CLASS_NAME, data)
            coin_data = extract_gate_coin_data(coins_data_list)
        elif option == 'kc':
            print("\n\nKUCOIN")
            COIN_DIV_CLASS_NAME = '(<tr .*?<\/tr>)'
            coins_data_list = re.findall(COIN_DIV_CLASS_NAME, data)
            coin_data = extract_kucoin_coin_data(coins_data_list)

    except Exception as e:
        print('\n\nCATCH! -> ', str(e), '\n\n')
        coin_data = pd.DataFrame()

    return coin_data


def extract_binance_coin_data(coins_data):
    COIN_DATA_EXTRACT = '>(.*?)<'
    coin_dataFrame = pd.DataFrame()

    name_list = []
    price_list = []
    change_list = []
    high_low_list = []
    volume_list = []
    marketcap_list = []

    for i in range(len(coins_data)):
        cur_str = str(coins_data[i]).strip("()'")
        # print(cur_str)
        regex_resault = re.findall(COIN_DATA_EXTRACT, cur_str)

        l = []

        tmp_list = []
        for cur in regex_resault:
            if cur != '':
                tmp_list.append(cur)
        regex_resault = tmp_list[::]

        for i in range(len(regex_resault)):
            if regex_resault[i] != '' and ('Trade' not in regex_resault[i]) and ('Detail' not in regex_resault[i]):
                l.append(str(regex_resault[i]).strip("()'"))

        short_name, full_name, price1, price2, change, high_low, volume, market_cap = l[
            :8:]

        name_list.append(short_name+full_name)
        price_list.append(price1+price2)
        change_list.append(change)
        high_low_list.append(high_low)
        volume_list.append(volume)
        marketcap_list.append(market_cap)

    coin_dataFrame["name"] = name_list
    coin_dataFrame["price"] = price_list
    coin_dataFrame["change"] = change_list
    coin_dataFrame["high_low"] = high_low_list
    coin_dataFrame["volume"] = volume_list
    coin_dataFrame["marketcap"] = marketcap_list
    return coin_dataFrame


def extract_gate_coin_data(coins_data):
    COIN_DATA_EXTRACT = '>(.*?)<'
    coin_dataFrame = pd.DataFrame()

    name_list = []
    price_list = []
    change_list = []
    high_low_list = []
    volume_list = []
    marketcap_list = []

    for i in range(len(coins_data)):
        cur_str = str(coins_data[i])
        # print(cur_str)
        regex_resault = re.findall(COIN_DATA_EXTRACT, cur_str)

        l = []

        tmp_list = []
        for cur in regex_resault:
            if cur != '':
                tmp_list.append(cur)
        regex_resault = tmp_list[::]
        # print(regex_resault)
        # sys.exit()

        for i in range(len(regex_resault)):
            if regex_resault[i] != '' and regex_resault[i] != ' ':
                l.append(str(regex_resault[i]).strip("()'"))
        # print(l)
        if len(l) == 12:
            short_name, _, _, _, full_name, price, change, high, low, volume, market_cap, _ = l[
                ::]
        else:
            short_name, _, _, full_name, price, change, high, low, volume, market_cap, _ = l[
                ::]

        name_list.append(short_name + '/' + full_name)
        price_list.append(price)
        change_list.append(change)
        high_low_list.append(high + '/' + low)
        volume_list.append(volume)
        marketcap_list.append(market_cap)

    coin_dataFrame["name"] = name_list
    coin_dataFrame["price"] = price_list
    coin_dataFrame["change"] = change_list
    coin_dataFrame["high_low"] = high_low_list
    coin_dataFrame["volume"] = volume_list
    coin_dataFrame["marketcap"] = marketcap_list
    return coin_dataFrame


def extract_bitmart_coin_data(coins_data):
    COIN_DATA_EXTRACT = '>(.*?)<'
    coin_dataFrame = pd.DataFrame()

    name_list = []
    price_list = []
    change_list = []
    high_low_list = []
    volume_list = []
    marketcap_list = []

    for i in range(len(coins_data)):
        cur_str = str(coins_data[i])
        # print(cur_str)
        regex_resault = re.findall(COIN_DATA_EXTRACT, cur_str)

        l = []

        tmp_list = []
        for cur in regex_resault:
            if cur != '':
                tmp_list.append(cur)
        regex_resault = tmp_list[::]
        # print(regex_resault)
        # sys.exit()

        for i in range(len(regex_resault)):
            if regex_resault[i] != '' and regex_resault[i] != ' ':
                l.append(str(regex_resault[i]).strip())
        # print(l)
        _, name, price1, price2, change, high, low, volume, _ = l[
            ::]
        market_cap = None

        name_list.append(name)
        price_list.append(price1 + price2)
        change_list.append(change)
        high_low_list.append(high + '/' + low)
        volume_list.append(volume)
        marketcap_list.append(market_cap)

    coin_dataFrame["name"] = name_list
    coin_dataFrame["price"] = price_list
    coin_dataFrame["change"] = change_list
    coin_dataFrame["high_low"] = high_low_list
    coin_dataFrame["volume"] = volume_list
    coin_dataFrame["marketcap"] = marketcap_list
    return coin_dataFrame


def extract_kucoin_coin_data(coins_data):
    COIN_DATA_EXTRACT = '>(.*?)<'
    coin_dataFrame = pd.DataFrame()

    name_list = []
    price_list = []
    change_list = []
    high_low_list = []
    volume_list = []
    marketcap_list = []

    for i in range(len(coins_data)):
        cur_str = str(coins_data[i])
        # print(cur_str)
        regex_resault = re.findall(COIN_DATA_EXTRACT, cur_str)

        l = []

        tmp_list = []
        for cur in regex_resault:
            if cur != '':
                tmp_list.append(cur)
        regex_resault = tmp_list[::]
        # print(regex_resault)
        # sys.exit()

        for i in range(len(regex_resault)):
            if regex_resault[i] != '' and regex_resault[i] != ' ':
                l.append(str(regex_resault[i]).strip())
        print("KU LEN :", len(l), l)
        if len(l) == 12:
            name, _, _, price1, price2, _, change, _, _, _, _, _ = l[
                ::]
        else:
            name, _, _, price1, _, price2, _, change, _, _, _, _, _ = l[
                ::]
        market_cap = None
        high_low = None
        volume = None

        name_list.append(name)
        price_list.append(price1 + price2)
        change_list.append(change)
        high_low_list.append(high_low)
        volume_list.append(volume)
        marketcap_list.append(market_cap)

    coin_dataFrame["name"] = name_list
    coin_dataFrame["price"] = price_list
    coin_dataFrame["change"] = change_list
    coin_dataFrame["high_low"] = high_low_list
    coin_dataFrame["volume"] = volume_list
    coin_dataFrame["marketcap"] = marketcap_list
    return coin_dataFrame


if __name__ == "__main__":
    op = extract_coin_data(
        open('../results/binance1.txt', 'r').read(), option='bn')
    # op = extract_coin_data(
    #     open('../results/bitmart1.txt', 'r').read(), option='bm')
    # op = extract_coin_data(
    #     open('../results/gate1.txt', 'r').read(), option='g')
    # op = extract_coin_data(
    #     open('../results/kucoin1.txt', 'r').read(), option='kc')
    # print(type(op))
    print(op)

    # s = ''.join(open('../results/bitmart1.txt', 'r').read().split('\t'))
    # open('../results/bitmart1.txt', 'w').write(s)
