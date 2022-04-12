from datetime import datetime
from typing import List
import numpy as np
import MetaTrader5 as mt5
from pytz import timezone
import data.settings as data_settings
import model.settings as model_settings


def get_initial_data(model_date: str = model_settings.model_name, symbol: str = data_settings.symbol) -> tuple[List, List]:

    # Make model date's time compatible with metatradertimesone
    model_date = datetime.strptime(model_date, "%y-%m-%d %H:%M:%S")
    model_date = convert_to_metatrader_timezone(model_date)

    if not mt5.initialize():
        print("initialize() failed")
        mt5.shutdown()

    now = convert_to_metatrader_timezone(datetime.now())

    data_until_now = mt5.copy_rates_range(
        symbol, mt5.TIMEFRAME_M5, model_date, now)

    data_before_model_date = mt5.copy_rates_from(
        symbol, mt5.TIMEFRAME_M5, model_date, data_settings.how_many_candles_before)

    return data_until_now.tolist(), data_before_model_date.tolist()


def get_live_data():
    return


def load_data_from_csv():
    return


def convert_to_metatrader_timezone(date: datetime) -> datetime:
    date = datetime.fromtimestamp(
        int(date.timestamp()) + data_settings.time_difference_in_seconds)
    return date


if __name__ == "__main__":
    pass

    # chill
