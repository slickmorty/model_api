from datetime import datetime
from keras.models import load_model
import requests
import pandas as pd
import time
import logging
from pympler import asizeof

from data.settings import data_settings
from data import get_data, indicators
from model import model_update, predict
from model.settings import model_settings
from api import api_requests
from logs import logs


mylogs = logging.getLogger(__name__)


def main(send_to_database: bool = True):

    data_until_now, df, raw_df = get_and_save_initial_data()

    # Delete all previous data in database
    if send_to_database:
        delete_all_data_in_database()

    # Adding all new data in database(only some of the new ones)
    if send_to_database:
        add_all_new_data_in_database(df=df[-data_settings.window_size:])

    counter = len(data_until_now)

    # Check if the model needs to be updated initially
    if(len(data_until_now) >= data_settings.future_window_size*2):

        counter = data_settings.future_window_size

        mylogs.critical(logs.UPDATE_MODEL_INITIALLY)
        model, data = model_update.update_model_with_initial_info(df)
        mylogs.info(logs.FINISHED_UPDATING)
    else:
        mylogs.info(logs.LOADING)
        model = load_model(model_settings.model_path)

    mylogs.info(logs.PREDICTING)
    prediction = predict.predict(model, df, True)

    # Append all new data in a all_so_far_dataframe
    all_so_far = pd.read_csv(data_settings.all_data_so_far_path)

    temp_df = df[df.TimeStamp > all_so_far.TimeStamp.iloc[-1]]
    temp_df = temp_df[temp_df.Prediction != -1].reset_index(drop=True)

    all_so_far = pd.concat([all_so_far, temp_df], ignore_index=True)
    all_so_far.to_csv(data_settings.all_data_so_far_path, index=False)

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
            df_copy = df_copy[-data_settings.window_size:
                              ].reset_index(drop=True)

            # Predict
            predict.predict(model, df_copy)

            # َADD to data frame and save
            mylogs.warning(logs.SAVING_CAREFULL)
            df.loc[len(df)] = df_copy.iloc[-1]
            df.to_csv(data_settings.indicator_data_csv_path, index=False)

            # Add to all_so_far
            all_so_far.loc[len(all_so_far)] = df_copy.iloc[-1]
            all_so_far.to_csv(data_settings.all_data_so_far_path, index=False)

            # Check for model update here
            mylogs.warning(logs.WAITING_FOR_NEXT_CANDLE)

            # Convert DateTime to str so can be sendable in json
            df.loc[len(df)-1:, "DateTime"] = df.iloc[-1:].DateTime.astype(str)

            # Adding all new data in database
            if send_to_database:
                add_new_data_in_database(df=df.iloc[-1:])

            print(
                f'candles to update: {(data_settings.future_window_size * 2)-counter}')

            counter += 1

        # Check if the model needs to be updated
        if(counter >= data_settings.future_window_size * 2):

            model = update_the_model(df, model)
            counter = 24

            # Very very wierd memory management issue is solved with this
            # Holy shit wtf is this
            model = load_model(model_settings.model_path)

            for key, value in locals().items():
                print(key, " : ", asizeof.asizeof(value) / 1024*1024, " MB")

            # for key, value in globals().items():
            #     print(key, " : ", asizeof.asizeof(value) / 1024*1024, " MB")

        time.sleep(1)


def update_the_model(df, model):
    # update Real column
    df = indicators.add_class(df)
    df.to_csv(data_settings.indicator_data_csv_path, index=False)

    mylogs.critical(logs.UPDATING_MODEL)
    new_model, _ = model_update.update_model(
        df[-data_settings.window_size-data_settings.future_window_size*2:], model=model)
    return new_model


def delete_all_data_in_database() -> requests.Response:

    response = requests.Response()
    while response.status_code != requests.status_codes.codes["okay"]:
        try:
            mylogs.info(logs.DELETING_ALL_DATA)
            response = api_requests.delete_all()
            mylogs.info(response)
        except Exception as e:
            mylogs.critical(logs.TRY_FAILED)
            print(e)
            time.sleep(5)
    return response


def add_all_new_data_in_database(df: pd.DataFrame) -> requests.Response:

    response = requests.Response()
    while response.status_code != requests.status_codes.codes["created"]:
        try:
            mylogs.warning(logs.ADDING_NEW_DATA)
            response = api_requests.insert_all(df=df[-256:])
            mylogs.info(response)
        except Exception as e:
            mylogs.critical(logs.TRY_FAILED)
            print(e)
            time.sleep(5)
    return response


def add_new_data_in_database(df: pd.DataFrame) -> requests.Response:
    response = requests.Response()
    while response.status_code != requests.status_codes.codes["created"]:
        try:
            mylogs.warning(logs.ADDING_NEW_DATA)
            response = api_requests.insert_one(df=df)
            mylogs.info(response)
        except Exception as e:
            mylogs.critical(logs.TRY_FAILED)
            print(e)
            time.sleep(5)
    return response


def get_and_save_initial_data() -> tuple[list, pd.DataFrame, pd.DataFrame]:
    logs.start(mylogs)
    mylogs.info(logs.GET_INITIAL_DATA)
    data_until_now, data_before_model_date = get_data.get_initial_data()
    # Delete last Data cause candle is not complete yet
    data_until_now.pop()

    mylogs.info(logs.CONVERT_TO_CSV)
    df, raw_df = get_data.convert_initial_data_to_pandas(
        data_until_now, data_before_model_date)

    # Data until now is in meta timezone
    # make datetime in data frame a str so i can send it in json
    df.DateTime = df.DateTime.astype(str)
    return data_until_now, df, raw_df


def get_new_candle() -> list:
    mylogs.info(logs.GETTING_NEW_DATA)
    # GET NEW CANDLE
    prev_candle = list(get_data.get_prev_candle())

    # convert to metatrader time and also to datetime object
    prev_candle_datetime = get_data.convert_from_metatrader_timezone(
        datetime.fromtimestamp(prev_candle[0]))

    prev_candle[0] += data_settings.time_difference_in_seconds
    # Inserting date time in index 0 in the list so the format would be
    # like this " datetime,timestamp,Open,High,Low,Close,tick_volume,spread,Volume "
    prev_candle.insert(0, prev_candle_datetime)
    return prev_candle


if __name__ == "__main__":
    logs.make_logs(logs=mylogs)

    try:
        main()

    except KeyboardInterrupt:
        for i in range(5):
            print("Exiting in ", 5-i, "*"*5-i, end="\r")
            time.sleep(1)
        mylogs.exception(logs.EXITING)
        exit()
    except Exception as e:
        mylogs.exception(e)
