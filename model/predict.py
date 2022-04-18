from tensorflow import keras
import pandas as pd
from data import DataProcessing, settings as data_settings


def predict(model: keras.Model, df: pd.DataFrame, save: bool = False) -> list[int]:

    prediction = [-1 for i in range(data_settings.window_size-1)]
    
    data = DataProcessing(
        data=df[:],
        input_width=data_settings.window_size,
        stockname=data_settings.symbol,
        minimum=-1.0,
        maximum=1.0
    )
    
    in_data = data.make_windows(data.scaled_data)
    model_predictions = model.predict(in_data)

    for _, value in enumerate(model_predictions):
        if(value[0] > 0.5):
            prediction.append(0)
        else:
            prediction.append(1)

    df["Prediction"] = prediction
    if(save):
        df.to_csv(data_settings.indicator_data_csv_path, index=False)
    return prediction
