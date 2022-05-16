from datetime import datetime
import MetaTrader5 as mt5
import pandas as pd
import time

from data.settings import data_settings
from model.settings import model_settings
from data import indicators
from logs import logs

from main import mylogs
logs.make_logs(logs=mylogs)


def get_initial_data(model_date: datetime = model_settings.model_date, symbol: str = data_settings.symbol) -> tuple[list, list]:

    # Make model date's time compatible with metatradertimesone
    model_date = convert_to_metatrader_timezone(model_date)

    now = convert_to_metatrader_timezone(datetime.now())
    if not mt5.initialize():
        mylogs.exception(logs.META_INITIALIZE_FAILED)
        mylogs.exception(mt5.last_error())
        mt5.shutdown()

    while True:
        try:
            data_until_now = mt5.copy_rates_range(
                symbol, mt5.TIMEFRAME_M5, model_date, now)

            data_before_model_date = mt5.copy_rates_from(
                symbol, mt5.TIMEFRAME_M5, model_date, data_settings.how_many_candles_before)

            if data_until_now is not None:
                data_until_now = data_until_now.tolist()
            else:
                raise Exception("Unable to retrieve Data")

            if data_before_model_date is not None:
                data_before_model_date = data_before_model_date.tolist()
            else:
                raise Exception("Unable to retrieve Data")

        except:
            mylogs.exception(logs.ERROR_RETRIEVING_DATA_FROM_META)
            mylogs.exception(mt5.last_error())
            if not mt5.initialize():
                mylogs.exception(logs.META_INITIALIZE_FAILED)
                mylogs.exception(mt5.last_error())
                mt5.shutdown()
            time.sleep(5)
        else:
            break

    return data_until_now, data_before_model_date


def get_live_data(symbol: str = data_settings.symbol) -> list[tuple]:

    # For when internet goes down
    while True:
        try:
            live_data = mt5.copy_rates_from_pos(
                symbol, mt5.TIMEFRAME_M5, 0, 1)

            if live_data is not None:
                live_data = live_data.tolist()
            else:
                raise Exception("Unable to retrieve Data")

        except Exception:
            mylogs.exception(logs.ERROR_RETRIEVING_DATA_FROM_META)
            mylogs.exception(mt5.last_error())
            if not mt5.initialize():
                mylogs.exception(logs.META_INITIALIZE_FAILED)
                mylogs.exception(mt5.last_error())
                mt5.shutdown()
            time.sleep(5)
        else:
            break

    return live_data


def get_prev_candle(symbol: str = data_settings.symbol) -> tuple:

    # For when internet goes down
    while True:
        try:
            # Old
            # prev_candle = mt5.copy_rates_from(
            #     symbol, mt5.TIMEFRAME_M5, convert_to_metatrader_timezone(datetime.now()), 2)

            prev_candle = mt5.copy_rates_from_pos(
                symbol, mt5.TIMEFRAME_M5, 0, 2)

            if prev_candle is not None:
                prev_candle = prev_candle.tolist()[:][0]
            else:
                raise Exception("Unable to retrieve Data")

        except Exception:
            mylogs.exception(mt5.last_error())
            mylogs.exception(logs.ERROR_RETRIEVING_DATA_FROM_META)
            if not mt5.initialize():
                mylogs.exception(logs.META_INITIALIZE_FAILED)
                mylogs.exception(mt5.last_error())
                mt5.shutdown()
            time.sleep(5)
        else:
            break
    return prev_candle


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
