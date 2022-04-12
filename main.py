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
    df = df.drop(labels=[i for i in range(34)], axis=0)
    df = df.reset_index()
    df.pop("index")
    df.to_csv("test.csv")

    return df


def main():
    # a, b = get_data.get_initial_data()

    # c = b+a
    # d = []
    # for i in c:

    #     asd = i[0]
    #     asd = datetime.fromtimestamp(asd)
    #     asd = get_data.convert_from_metatrader_timezone(asd)
    #     d.append((asd, i[1], i[2], i[3], i[4], i[5], i[6], i[7]))

    # df = pd.DataFrame(d, columns=data_settings.column_names)
    # df = indicators.add_indicators(df)
    # df = indicators.add_candles(df)
    # df = df.drop(labels=[i for i in range(34)], axis=0)
    # df = df.reset_index()
    # df.pop("index")
    # df.to_csv("test.csv")
    data_until_now, date_befor_model_date = get_data.get_initial_data()
    df = get_data_convet_to_pandas(data_until_now, date_befor_model_date)
    # breakpoint()


if __name__ == "__main__":
    main()
