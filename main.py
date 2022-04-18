from datetime import datetime
from http.client import ImproperConnectionState
from keras.models import load_model

from data import get_data, settings as data_settings, indicators, DataProcessing
from model import model_update, predict, settings as model_settings
from logs import logs
import numpy as np
import pandas as pd
import time

import logging
mylogs = logging.getLogger(__name__)


def main():
    logs.start(mylogs)
    mylogs.info(logs.GET_INITIAL_DATA)
    data_until_now, data_before_model_date = get_data.get_initial_data()
    # Delete last Data cause candle is not complete yet
    data_until_now.pop()

    mylogs.info(logs.CONVERT_TO_CSV)
    df, raw_df = get_data.convert_initial_data_to_pandas(
        data_until_now, data_before_model_date)

    # if(len(data_until_now) >= 48):

    #     mylogs.critical(logs.UPDATE_MODEL_INITIALLY)
    #     model, data = model_update.update_model_with_initial_info(df)
    #     mylogs.info(logs.FINISHED_UPDATING)

    # else:
    #     model = load_model(model_settings.model_path)

    # prediction = predict.predict(model, df,True)

    while(True):

        prev_candle = list(get_data.get_prev_candle())
        prev_candle[0] = get_data.convert_from_metatrader_timezone(
            datetime.fromtimestamp(prev_candle[0]))

        print(raw_df.tail(10))

        if(raw_df.iloc[-1].DateTime != prev_candle[0]):
            df_copy = raw_df.copy()
            # SAVE LIST IN DATAFRAME
            df_copy.loc[len(df_copy)] = prev_candle

            df_copy = indicators.add_indicators(df)
            df_copy = indicators.add_candles(df)
            df_copy = indicators.add_class(df)
            df_copy = df.iloc[]
            predict.predict(model, df_copy)

        # prev_candle = pd.Series(
        #     prev_candle, index=data_settings.column_names)
        # print(prev_candle)
        # # print(raw_raw_df.tail())
        # # print(prev_candle)

        # #     raw_df = pd.concat([raw_df, prev_candle])
        # #     print(raw_df.tail())
        # raw_df.add
        # print(raw_df.iloc[-1].DateTime == prev_candle[0])
        time.sleep(10)
    # get prev candle
    # check if its different
    # if it is , add to df


if __name__ == "__main__":
    logs.make_logs(logs=mylogs)
    main()
