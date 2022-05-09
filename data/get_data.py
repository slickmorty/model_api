from datetime import datetime
import MetaTrader5 as mt5
from data.settings import data_settings
from model.settings import model_settings
from data import indicators
import pandas as pd


def get_initial_data(model_date: datetime = model_settings.model_date, symbol: str = data_settings.symbol) -> tuple[list, list]:
    """Getting initial data

    Args:
        model_date (str, optional): The date model was previously trained on. Defaults to model_settings.model_date.
        symbol (str, optional): symbol e.g. SP500m. Defaults to data_settings.symbol.

    Returns:
        tuple[list, list]: A tuple containing list of data untill now and some data before model's date
    """

    # Make model date's time compatible with metatradertimesone
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
    if not mt5.initialize():
        print("initialize() failed")
        mt5.shutdown()
    live_data = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_M5, 0, 1)

    return live_data.tolist()


def get_prev_candle(symbol: str = data_settings.symbol) -> tuple:
    """Getting previous candle

    Args:
        symbol (str, optional): symbol e.g. SP500m. Defaults to data_settings.symbol.

    Returns:
        list[tuple]: A tuple containing data.
    """
    if not mt5.initialize():
        print("initialize() failed")
        mt5.shutdown()
    prev_candle = mt5.copy_rates_from(
        symbol, mt5.TIMEFRAME_M5, convert_to_metatrader_timezone(datetime.now()), 2)

    return prev_candle.tolist()[:][0]


def convert_to_metatrader_timezone(date: datetime) -> datetime:
    date = datetime.fromtimestamp(
        int(date.timestamp()) + data_settings.time_difference_in_seconds)
    return date


def convert_from_metatrader_timezone(date: datetime) -> datetime:

    date = datetime.fromtimestamp(
        int(date.timestamp()) - data_settings.time_difference_in_seconds)
    return date


def convert_initial_data_to_pandas(data_until_now: list, data_before_model_date: list, test: bool = False) -> tuple[pd.DataFrame, pd.DataFrame]:

    if not test:
        data_with_indicator_path = data_settings.indicator_data_csv_path
        raw_data_path = data_settings.raw_data_csv_path
    else:
        data_with_indicator_path = data_settings.indicator_test_data_csv_path
        raw_data_path = data_settings.raw_test_data_csv_path

    total = []
    for value in data_before_model_date+data_until_now:
        date = convert_from_metatrader_timezone(
            datetime.fromtimestamp(value[0]))
        timestamp = date.timestamp()
        total.append(
            (date, timestamp, value[1], value[2], value[3], value[4], value[5], value[6], value[7]))

    df = pd.DataFrame(total, columns=data_settings.column_names)
    raw_df = df.copy()
    # TODO: saving raw data remove if not needed
    df.to_csv(raw_data_path, index=False)

    df = indicators.add_indicators(df)
    df = indicators.add_candles(df)
    df = indicators.add_class(df)
    df = df.drop(labels=[i for i in range(
        data_settings.candles_with_nan)], axis=0)
    df = df.reset_index()
    df.pop("index")
    df.to_csv(data_with_indicator_path, index=False)

    return df, raw_df


if __name__ == "__main__":
    pass

    # chill
