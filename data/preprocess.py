import pandas as pd
from data.settings import data_settings
import numpy as np
from tensorflow import one_hot


class DataProcessing():

    def __init__(
            self, data: pd.core.frame.DataFrame,
            input_width: int = data_settings.window_size,
            stockname: str = data_settings.symbol,
            minimum: float = -1.0, maximum: float = 1.0):

        data.pop("DateTime")
        self.data = pd.DataFrame()
        for column in data_settings.indicators+data_settings.candle_params:
            self.data[f"{column}"] = data[f"{column}"]

        self.output = data.pop("Real")
        self.stockname: str = stockname
        self.input_width: int = input_width
        self.data_mean = self.data.mean()
        self.data_std = self.data.std()

        self.scaled_data, _, _ = self.normalize(
            self.data, data_std=self.data_std, data_mean=self.data_mean)  # TODO ? idk what the fuck to do with data mean and datastd probably doesnt even matter
        # I know its wrong fuck off
        self.scaled_data = self.min_max_scaler(self.scaled_data, minimum, maximum)

    def make_windows(self, input_data: pd.core.frame.DataFrame, output_data: pd.core.series.Series = None, convert_to_numpy: bool = True):

        window_input = []

        if output_data is None:
            for i in range(self.input_width, len(input_data)+1):

                window_input.append(
                    input_data[i-self.input_width:i].reset_index())

                window_input[-1].pop("index")

                # convert pd.DataFrame to numpy
                window_input[-1] = window_input[-1].to_numpy()

            # convert list to numpy

            if(convert_to_numpy):
                window_input = np.asarray(window_input)

            return window_input

        else:
            window_output = []
            for i in range(self.input_width, len(input_data)):

                window_input.append(
                    input_data[i-self.input_width:i].reset_index())
                window_output.append(output_data[i-1])
                window_input[-1].pop("index")
                # convert pd.DataFrame to numpy
                window_input[-1] = window_input[-1].to_numpy()

            # convert list to numpy

            if(convert_to_numpy):
                window_input = np.asarray(window_input)
                window_output = np.asarray(window_output)

                window_output = one_hot(window_output, depth=2)

            return window_input, window_output

    @staticmethod
    def normalize(data: pd.core.frame.DataFrame, data_std=None, data_mean=None):
        if(data_std is None):
            data_std = data.std()
        if(data_mean is None):
            data_mean = data.mean()

        data_normalized = (data-data_mean)/data_std

        return data_normalized, data_std, data_mean

    @staticmethod
    def min_max_scaler(data: pd.core.frame.DataFrame, minimum: float, maximum: float):
        data_max = data.describe().transpose()["max"]
        data_min = data.describe().transpose()["min"]
        data_std = (data-data_min)/(data_max-data_min)
        data_scaled = data_std*(abs(minimum)+maximum)+minimum
        return data_scaled

    @property
    def windows(self):
        return self.make_windows(
            input_data=self.scaled_data,
            output_data=self.output,
            convert_to_numpy=True)
    