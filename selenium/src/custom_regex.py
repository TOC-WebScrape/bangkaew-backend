import re

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

        coin_data = {}
        cnt = 0
        for i in range(len(coins_data)):
            cur_str = str(coins_data[i]).strip("()'")
            regex_resault = re.findall(COIN_DATA_EXTRACT, cur_str)
            l = []
            for i in range(len(regex_resault)):
                if regex_resault[i] != '' and ('Trade' not in regex_resault[i]) and ('Detail' not in regex_resault[i]):
                    l.append(str(regex_resault[i]).strip("()'"))
            short_name, full_name, price, change, volume, market_cap = l[:6:]
            tmp_coin_data = {
                "short_name": short_name,
                "full_name": full_name,
                "price": price,
                "change": change,
                "volume": volume,
                "market_cap": market_cap,
            }
            coin_data.update({cnt: tmp_coin_data})
            cnt += 1

    except:
        coin_data = {}

    return coin_data


if __name__ == "__main__":
    op = extract_coin_data(open('dummy.txt', 'r').read())
    print(op)
