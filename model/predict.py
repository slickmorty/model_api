from tensorflow import keras
import pandas as pd
from data import DataProcessing,settings as data_settings


def predict(model: keras.Model, df: pd.DataFrame):

    prediction = [-1 for i in range(256)]
    data =DataProcessing(
        data=df,
        input_width=data_settings.window_size,
        stockname=data_settings.symbol,
        minimum=-1.0,
        maximum=1.0
    )
    in_data = data.make_windows(data.data)
    model_predictions = model.predict(in_data)
