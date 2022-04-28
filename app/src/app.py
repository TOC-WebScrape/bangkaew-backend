import re
from fastapi import FastAPI, responses
import pandas as pd

app = FastAPI()

# test_str = ("BTC/USDT\n"
#             "DOGE/USDT\n"
#             "ETH/USDT\n"
#             "APE/USDT\n"
#             "BUSD/USDT\n"
#             "GMT/USDT\n"
#             "LUNA/USDT\n"
#             "BNB/USDT\n"
#             "SHIB/USDT\n"
#             "NEAR/USDT\n"
#             "UST/USDT\n"
#             "XRP/USDT\n"
#             "SOL/USDT\n"
#             "USDC/USDT\n"
#             "JASMY/USDT\n"
#             "ROSE/USDT\n"
#             "ADA/USDT\n"
#             "AVAX/USDT\n"
#             "RUNE/USDT\n"
#             "DOT/USDT\n"
#             "SLP/USDT\n"
#             "FTM/USDT\n"
#             "ZIL/USDT\n"
#             "CAKE/USDT\n"
#             "TRX/USDT\n"
#             "KNC/USDT\n"
#             "SAND/USDT\n"
#             "MATIC/USDT\n"
#             "GALA/USDT\n"
#             "GRT/USDT\n"
#             "WAVES/USDT\n"
#             "ATOM/USDT\n"
#             "ZRX/USDT\n"
#             "KAVA/USDT\n"
#             "EOS/USDT\n"
#             "FIL/USDT\n"
#             "LINK/USDT\n"
#             "AAVE/USDT\n"
#             "XMR/USDT\n"
#             "EUR/USDT\n"
#             "VET/USDT\n"
#             "ETC/USDT\n"
#             "MANA/USDT\n"
#             "LTC/USDT\n"
#             "AXS/USDT\n"
#             "CRV/USDT\n"
#             "SNX/USDT\n"
#             "ENS/USDT\n"
#             "GLMR/USDT\n"
#             "DAR/USDT")


FILENAMES = ["bn", "bm", "g", "kc"]


def get_name_currency_list():
    names = {}
    list_name = []
    for filename in FILENAMES:
        try:
            df = pd.read_csv(f"./data/{filename}.csv")
            list_name = df["name"].tolist()
            for n in list_name:
                x = n+'\n'
                names[x] = names.get(x, None)
        except:
            continue
    return "\n".join(names.keys())


CURRENCY_NAME = get_name_currency_list()


def get_data_currency(currency_name: str, cex: str):
    data = {}
    for filename in cex:
        try:
            df = pd.read_csv(f"./data/{filename}.csv")
            data[filename] = df.loc[df["name"] ==
                                    f"{currency_name.upper()}"].to_dict()
        except:
            break
    return data


@app.get("/api/suggest")
async def suggestion(text: str = ""):
    if len(text) == 0:
        return "Please type something"
    try:
        matches = re.findall(r".*{0}.*".format(text),
                             CURRENCY_NAME, re.IGNORECASE | re.MULTILINE)
    except TypeError:
        return responses.JSONResponse({"Error": "Currency name not found"}, 500)
    return {"suggest": matches[:10]}


@app.get("/api/currency/{name}")
async def currency(name: str, cex: str = "bn,bm,g,kc"):
    cex = cex.split(',')
    name = name.replace(".", "/")
    return get_data_currency(name, cex)
