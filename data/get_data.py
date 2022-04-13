from datetime import datetime
from symtable import Symbol
import numpy as np
import MetaTrader5 as mt5
from pytz import timezone
import data.settings as data_settings
import model.settings as model_settings
import pandas as pd


def get_initial_data(model_date: str = model_settings.model_name, symbol: str = data_settings.symbol) -> tuple[list, list]:
    """Getting initial data

    Args:
        model_date (str, optional): The date model was previously trained on. Defaults to model_settings.model_name.
        symbol (str, optional): symbol e.g. SP500m. Defaults to data_settings.symbol.

    Returns:
        tuple[list, list]: A tuple containing list of data untill now and some data before model's date
    """
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


def get_live_data(symbol: str = data_settings.symbol) -> list[tuple]:
    """Getting Live data

    Args:
        symbol (str, optional): symbol e.g. SP500m. Defaults to data_settings.symbol.

    Returns:
        list[tuple]: A list containing a tuple containing data.
    """
    live_data = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_M5, 0, 1)

    return live_data.tolist()


def get_prev_candle(symbol: str = data_settings.symbol) -> tuple:
    """Getting previous candle

    Args:
        symbol (str, optional): symbol e.g. SP500m. Defaults to data_settings.symbol.

    Returns:
        list[tuple]: A tuple containing data.
    """
    prev_candle = mt5.copy_rates_from(
        symbol, mt5.TIMEFRAME_M5, convert_to_metatrader_timezone(datetime.now()), 2)

    return prev_candle.tolist()[:][0]


def load_data_from_csv():
    return


def convert_to_metatrader_timezone(date: datetime) -> datetime:
    date = datetime.fromtimestamp(
        int(date.timestamp()) + data_settings.time_difference_in_seconds)
    return date


def convert_from_metatrader_timezone(date: datetime) -> datetime:

    date = datetime.fromtimestamp(
        int(date.timestamp()) - data_settings.time_difference_in_seconds)
    return date


if __name__ == "__main__":
    pass

    # chill
