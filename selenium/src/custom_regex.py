import re
import pandas as pd

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


def extract_coin_data(data, option='binance'):

    try:
        if option == 'binance':
            COIN_DIV_CLASS_NAME = '((<div direction=\"ltr\".*?)Trade)'
            COIN_DATA_EXTRACT = '>(.*?)<'

        coins_data = re.findall(COIN_DIV_CLASS_NAME, data)

        coin_data = pd.DataFrame()
        cnt = 0

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

            # tmp_coin_data = {
            #     "name": short_name + full_name,
            #     "price": price1 + price2,
            #     "change": change,
            #     "hight_low": high_low,
            #     "volume": volume,
            #     "market_cap": market_cap,
            # }
            # coin_data.update({cnt: tmp_coin_data})
            # cnt += 1

            name_list.append(short_name+full_name)
            price_list.append(price1+price2)
            change_list.append(change)
            high_low_list.append(high_low)
            volume_list.append(volume)
            marketcap_list.append(market_cap)

        coin_data["name"] = name_list
        coin_data["price"] = price_list
        coin_data["change"] = change_list
        coin_data["high_low"] = high_low_list
        coin_data["volume"] = volume_list
        coin_data["marketcap"] = marketcap_list

    except:
        print('CATCH!')
        coin_data = pd.DataFrame()

    return coin_data


if __name__ == "__main__":
    op = extract_coin_data(open('../results/binance1.txt', 'r').read())
    # print(type(op))
    print(op)
