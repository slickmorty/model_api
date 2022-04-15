import json


with open("./data/settings.json", "r") as f:
    data: dict = json.load(f)

symbol = data.get("symbol")
how_many_candles_before = data.get("how_many_candles_before")
candles_with_nan = data.get("candles_with_nan")
time_difference_in_seconds = data.get("data").get("time_difference_in_seconds")
column_names = data.get("column_names")
raw_data_csv_path = data.get("raw_data_csv_path")
indicator_data_csv_path = data.get("data").get("indicator_data_csv_path")
indicators = data.get("indicators")
candle_params = data.get("candle_params")
window_size = data.get("window_size")
future_window_size = data.get("future_window_size")
