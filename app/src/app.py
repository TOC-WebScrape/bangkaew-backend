import os
import re
import typing
from fastapi import FastAPI, responses
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import orjson
import pandas as pd


class ORJSONResponse(JSONResponse):
    media_type = "application/json"

    def render(self, content: typing.Any) -> bytes:
        return orjson.dumps(content, option=orjson.OPT_NON_STR_KEYS)


app = FastAPI()

origins = os.getenv('CORS').split(',')

app.add_middleware(CORSMiddleware,
                   allow_origins=['*'],
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"],)


FILENAMES = ["bn", "bm", "g", "kc"]


def get_name_currency_list():
    names = {}
    list_name = []
    for filename in FILENAMES:
        try:
            df = pd.read_csv(f"./data/{filename}.csv")
            for i in df["name"].tolist():
                list_name.append(i.split('/')[0])
            for n in list_name:
                names[n] = names.get(n, None)
        except:
            continue
    return list(names.keys())


CURRENCY_NAME = get_name_currency_list()


def get_data_currency(currency_name: str, cex: str):
    data = {}
    for filename in cex:
        try:
            df = pd.read_csv(f"./data/{filename}.csv")
            df.set_index('name', inplace=True)
            data[filename] = df.loc[df.index.str.contains(
                f"{currency_name.upper()}")].to_dict()
        except:
            continue
    return data


@app.get("/api/currency-name")
async def suggestion():
    return {"result": CURRENCY_NAME}


@app.get("/api/currency/{name}", response_class=ORJSONResponse)
async def currency(name: str, cex: str = "bn,bm,g,kc"):
    cex = cex.split(',')
    return get_data_currency(name, cex)
