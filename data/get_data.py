from datetime import datetime
from importlib.resources import Package
import MetaTrader5 as mt5
import data.settings as data_settings
import model.settings as model_settings


def get_initial_data(model_date: str = model_settings.model_name, symbol: str = data_settings.symbol) -> tuple:

    model_date = datetime.strptime(model_date, "%y-%m-%d %H:%M:%S")
    if not mt5.initialize():
        print("initialize() failed")
        mt5.shutdown()

    data_until_now = mt5.copy_rates_range(
        symbol, mt5.TIMEFRAME_M5, model_date, datetime.now())

    data_before_model_date = mt5.copy_rates_from(
        symbol, mt5.TIMEFRAME_M5, model_date, data_settings.how_many_candles_before)

    return data_until_now, data_before_model_date


def get_live_data():
    return


def load_data_from_csv():
    return


if __name__ == "__main__":

    # chill
