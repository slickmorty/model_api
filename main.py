from datetime import datetime
from data import get_data, settings as data_settings, indicators, DataProcessing
from model import model_update, settings as model_settings
import numpy as np
from keras.models import load_model, save_model
import pandas as pd
import time


def get_initial_data_convet_to_pandas(data_until_now: list, data_befor_model_date: list) -> pd.DataFrame:

    total = []
    for value in data_befor_model_date+data_until_now:
        total.append((get_data.convert_from_metatrader_timezone(datetime.fromtimestamp(
            value[0])), value[1], value[2], value[3], value[4], value[5], value[6], value[7]))

    df = pd.DataFrame(total, columns=data_settings.column_names)

    # TODO: saving raw data remove if not needed
    df.to_csv(data_settings.raw_data_csv_path, index=False)

    df = indicators.add_indicators(df)
    df = indicators.add_candles(df)
    df = indicators.add_class(df)
    df = df.drop(labels=[i for i in range(
        data_settings.candles_with_nan)], axis=0)
    df = df.reset_index()
    df.pop("index")
    df.to_csv(data_settings.indicator_data_csv_path, index=False)

    return df


def update_model_with_initial_info(df: pd.DataFrame):

    data = DataProcessing(
        data=df[:-data_settings.future_window_size],
        input_width=data_settings.window_size,
        stockname=data_settings.symbol,
        minimum=-1.0,
        maximum=1.0
    )
    model = load_model(model_settings.base_model_path)
    input_window, output_window = data.windows
    model_update.compile_and_fit(model, input_window, output_window)
    model.save(model_settings.model_path)
    return model, data


def main():

    data_until_now, data_before_model_date = get_data.get_initial_data()

    df = get_initial_data_convet_to_pandas(
        data_until_now, data_before_model_date)

    model, data = update_model_with_initial_info(df)
    # breakpoint()


if __name__ == "__main__":
    main()
