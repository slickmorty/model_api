from datetime import datetime
from keras.models import load_model
from tensorflow import metrics
import requests
import pandas as pd

from data.settings import data_settings
from data import get_data, indicators
from model import model_update, predict
from model.settings import model_settings


def test():

    data_until_now, data_before_model_date = get_data.get_initial_data(
        model_date=model_settings.test_model_date)
    # Delete last Data cause candle is not complete yet
    data_until_now.pop()

    df, raw_df = get_data.convert_initial_data_to_pandas(
        data_until_now=[], data_before_model_date=data_before_model_date, test=True)

    for index, value in enumerate(data_until_now):

        # Getting latest completed candle
        prev_candle = get_new_candle(value=value)

        # Check if the candle is new
        if(raw_df.iloc[-1].DateTime != prev_candle[0]):

            df_copy = raw_df.copy()

            # SAVE LIST IN DATAFRAME
            df_copy.loc[len(df_copy)] = prev_candle

            # Save new data in raw_df
            raw_df.loc[len(raw_df)] = prev_candle
            raw_df.to_csv(data_settings.raw_data_csv_path, index=False)

            # Adding indicators
            df_copy = indicators.add_indicators(df_copy)
            df_copy = indicators.add_candles(df_copy)
            df_copy = indicators.add_class(df_copy)

            # Make it as small as possible
            df_copy = df_copy[-data_settings.window_size:
                              ].reset_index(drop=True)

            # Predict
            predict.predict(model, df_copy)

            # َADD to data frame and save
            df.loc[len(df)] = df_copy.iloc[-1]
            df.to_csv(data_settings.indicator_data_csv_path, index=False)

            # Check for model update here

            # Convert DateTime to str so can be sendable in json
            df.loc[len(df)-1:, "DateTime"] = df.iloc[-1:].DateTime.astype(str)

            # Adding all new data in database
            # add_new_data_in_database(df=df.iloc[-1:])

            print(
                f'candles to update: {(data_settings.future_window_size * 2)-len(df[df.Real == -1])}')

            # TODO COUNTER = +=1

        # Check if the model needs to be updated
        # TODO if(COUNTER >= FUTURE_WINDOW_SIZE)
        if(len(df[df.Real == -1]) >= data_settings.future_window_size * 2):

            model = update_the_model(df, model)
            # TODO COUNTER=0


def update_the_model(df, model):
    # update Real column
    df = indicators.add_class(df)
    df.to_csv(data_settings.indicator_data_csv_path, index=False)

    new_model, _ = model_update.update_model(
        df[-data_settings.window_size-data_settings.future_window_size*2:], model=model)
    return new_model


def delete_all_data_in_database() -> requests.Response:

    response = requests.Response()
    while response.status_code != requests.status_codes.codes["okay"]:
        try:
            response = api_requests.delete_all()
        except Exception as e:
            print(e)
            time.sleep(5)
    return response


def get_new_candle(value: tuple) -> list:

    # GET NEW CANDLE
    prev_candle = list(value)

    # convert to metatrader time and also to datetime object
    prev_candle_datetime = get_data.convert_from_metatrader_timezone(
        datetime.fromtimestamp(prev_candle[0]))

    prev_candle[0] += data_settings.time_difference_in_seconds
    # Inserting date time in index 0 in the list so the format would be
    # like this " datetime,timestamp,Open,High,Low,Close,tick_volume,spread,Volume "
    prev_candle.insert(0, prev_candle_datetime)
    return prev_candle


if __name__ == "__main__":
    test()
