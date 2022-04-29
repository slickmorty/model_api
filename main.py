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

    data_until_now, df, raw_df = get_save_initial_data()

    if(len(data_until_now) >= 48):

        mylogs.critical(logs.UPDATE_MODEL_INITIALLY)
        model, data = model_update.update_model_with_initial_info(df)
        mylogs.info(logs.FINISHED_UPDATING)

    else:
        mylogs.info(logs.LOADING)
        model = load_model(model_settings.model_path)

    mylogs.info(logs.PREDICTING)
    prediction = predict.predict(model, df, True)

    while(True):

        # Getting latest completed candle
        prev_candle = get_new_candle()

        # Check if the candle is new
        if(raw_df.iloc[-1].DateTime != prev_candle[0]):

            mylogs.warning(logs.NEW_CANDLE_DETECTED)
            df_copy = raw_df.copy()

            # SAVE LIST IN DATAFRAME
            df_copy.loc[len(df_copy)] = prev_candle

            # Save new data in raw_df
            mylogs.warning(logs.SAVING_CAREFULL)
            raw_df.loc[len(raw_df)] = prev_candle
            raw_df.to_csv(data_settings.raw_data_csv_path, index=False)

            # Adding indicators
            df_copy = indicators.add_indicators(df_copy)
            df_copy = indicators.add_candles(df_copy)
            df_copy = indicators.add_class(df_copy)

            # Make it as small as possible
            df_copy = df_copy[-256:].reset_index(drop=True)

            # Predict
            predict.predict(model, df_copy)

            # َADD to data frame and save
            mylogs.warning(logs.SAVING_CAREFULL)
            df.loc[len(df)] = df_copy.iloc[-1]
            df.to_csv(data_settings.indicator_data_csv_path, index=False)

            # Check for model update here
            mylogs.warning(logs.WAITING_FOR_NEXT_CANDLE)

            # time.sleep(270)

        time.sleep(1)


def get_save_initial_data():
    logs.start(mylogs)
    mylogs.info(logs.GET_INITIAL_DATA)
    data_until_now, data_before_model_date = get_data.get_initial_data()
    # Delete last Data cause candle is not complete yet
    data_until_now.pop()

    mylogs.info(logs.CONVERT_TO_CSV)
    df, raw_df = get_data.convert_initial_data_to_pandas(
        data_until_now, data_before_model_date)

    return data_until_now, df, raw_df


def get_new_candle():
    mylogs.info(logs.GETTING_NEW_DATA)
    # GET NEW CANDLE
    prev_candle = list(get_data.get_prev_candle())

    # convert to metatrader time and also to datetime object
    prev_candle_datetime = get_data.convert_from_metatrader_timezone(
        datetime.fromtimestamp(prev_candle[0]))

    prev_candle[1] += data_settings.time_difference_in_seconds
    # Inserting date time in index 0 in the list so the format would be
    # like this " datetime,timestamp,Open,High,Low,Close,tick_volume,spread,Volume "
    prev_candle.insert(0, prev_candle_datetime)
    return prev_candle


if __name__ == "__main__":
    logs.make_logs(logs=mylogs)
    main()
