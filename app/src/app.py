from fastapi import FastAPI
import pandas as pd
import re

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

filenames = ["bn", "bm", "g", "kc"]


def get_name_currency_list():
    names = {}
    for filename in filenames:
        data = pd.read_csv(f"../data/{filename}.csv")
        list_name = data["name"].tolist()
    for n in list_name:
        names[n] = names.get(n, None)
    return tuple(names.keys())


list_name = get_name_currency_list()


def get_data_currency(currency_id: str):
    data = {}
    for filename in filenames:
        df = pd.read_csv(f"../data/{filename}.csv")
        data[filename] = df.loc[df["name"] ==
                                f"{currency_id.upper()}/USDT"].to_dict()
    return data


@app.get("/api/suggest")
async def suggestion(text: str = ""):
    if len(text) == 0:
        return "Please type something"
    matches = re.findall(r".*{0}.*".format(text), list_name,
                         re.MULTILINE | re.IGNORECASE)
    return {"suggest": matches}


@app.get("/api/currency/{id}")
async def currency(id: str):
    return get_data_currency(id)
