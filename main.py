from datetime import datetime
import pandas
from data import get_data, settings as data_settings, indicators
import numpy as np
import pandas as pd
from typing import List


def get_data_convet_to_pandas(data_until_now: List, data_befor_model_date: List) -> pd.DataFrame:

    total = []
    for value in data_befor_model_date+data_until_now:
        total.append((get_data.convert_from_metatrader_timezone(datetime.fromtimestamp(
            value[0])), value[1], value[2], value[3], value[4], value[5], value[6], value[7]))

    df = pd.DataFrame(total, columns=data_settings.column_names)
    df = indicators.add_indicators(df)
    df = indicators.add_candles(df)
    df = df.drop(labels=[i for i in range(
        data_settings.candles_with_nan)], axis=0)
    df = df.reset_index()
    df.pop("index")
    df.to_csv(data_settings.csv_path)

    return df


def main():

    data_until_now, data_before_model_date = get_data.get_initial_data()
    df = get_data_convet_to_pandas(data_until_now, data_before_model_date)
    # breakpoint()


if __name__ == "__main__":
    main()
