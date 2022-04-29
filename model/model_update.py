from tensorflow import keras, metrics
from keras.models import load_model
import numpy as np
import pandas as pd

from data import DataProcessing
from data.settings import data_settings
from model.settings import model_settings


def compile_and_fit(model: keras.Model, input_window: np.ndarray, output_window: np.ndarray) -> None:

    model.compile(loss=model_settings.loss,
                  optimizer=model_settings.optimizer,
                  metrics=[metrics.BinaryAccuracy()])
    model.fit(
        x=input_window,
        y=output_window,
        batch_size=model_settings.batch_size,
        shuffle=True,
        epochs=model_settings.epoches,
    )
    return


def update_model_with_initial_info(df: pd.DataFrame) -> tuple[keras.Model, DataProcessing]:

    data = DataProcessing(
        data=df[:-data_settings.future_window_size],
        input_width=data_settings.window_size,
        stockname=data_settings.symbol,
        minimum=data_settings.min_value,
        maximum=data_settings.max_value
    )
    model = load_model(model_settings.model_path)
    input_window, output_window = data.windows
    compile_and_fit(model, input_window, output_window)

    model.save(model_settings.model_path)

    model_settings.model_date = df.iloc[-data_settings.future_window_size]["DateTime"]

    model_settings.save(param=str(model_settings.model_date),
                        param_name="model_date")

    return model, data
