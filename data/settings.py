import json


with open("./data/settings.json", "r") as f:
    data: dict = json.load(f)

symbol: str = data.get("symbol")
how_many_candles_before: int = data.get("how_many_candles_before")
candles_with_nan: int = data.get("candles_with_nan")
time_difference_in_seconds: int = data.get(
    "data").get("time_difference_in_seconds")
column_names: list[str] = data.get("column_names")
raw_data_csv_path: str = data.get("raw_data_csv_path")
indicator_data_csv_path: str = data.get("data").get("indicator_data_csv_path")
indicators: list[str] = data.get("indicators")
candle_params: list[str] = data.get("candle_params")
window_size: int = data.get("window_size")
future_window_size: int = data.get("future_window_size")


def save(param, param_name: str, data: dict = data):
    data[f"{param_name}"] = param

    with open("./data/settings.json", "w") as f:
        json.dump(data, f)
