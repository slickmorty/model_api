import json


class DataSettings():
    pass


data_settings = DataSettings()

with open("./data/settings.json", "r") as f:
    data: dict = json.load(f)

for key, value in data.items():
    setattr(data_settings, key, value)

# symbol: str = data.get("symbol")
# how_many_candles_before: int = data.get("how_many_candles_before")
# candles_with_nan: int = data.get("candles_with_nan")
# time_difference_in_seconds: int = data.get("time_difference_in_seconds")
# column_names: list[str] = data.get("column_names")
# raw_data_csv_path: str = data.get("raw_data_csv_path")
# indicator_data_csv_path: str = data.get("indicator_data_csv_path")
# indicators: list[str] = data.get("indicators")
# candle_params: list[str] = data.get("candle_params")
# window_size: int = data.get("window_size")
# future_window_size: int = data.get("future_window_size")
# max_value: float = data.get("max_value")
# min_value: float = data.get("min_value")


def save(param, param_name: str, data: dict = data):
    data[f"{param_name}"] = param

    with open("./data/settings.json", "w") as f:
        json.dump(data, f)
