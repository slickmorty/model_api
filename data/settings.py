import json


with open("./data/settings.json", "r") as f:
    data: dict = json.load(f)

symbol = data.get("data").get("symbol")
how_many_candles_before = data.get("data").get("how_many_candles_before")
