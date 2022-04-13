from tkinter import N
import pandas as pd
from data import settings
import settings as data_settings
import numpy as np
import tensorflow as tf


class DataProcessing():

    def __init__(self, data: pd.core.frame.DataFrame,
                 output: pd.core.series.Series,
                 input_width: int = settings.window_size,
                 stockname: str = data_settings.symbol,
                 min_max: bool = False, minimum: float = -1.0, maximum: float = 1.0):
        """init method of DataProcessing class

        Args:
            data (pd.core.frame.DataFrame): all of our data
            output (pd.core.series.Series): all of our outputs
            input_width (int): window size
            stockname (str): stock name 
            min_max (bool, optional):  whether we want min_max scaling. Defaults to False.
            minimum (float, optional): mininum of scaled data. Defaults to -1.0.
            maximum (float, optional): maximum of scaled data. Defaults to 1.0.
        """
        self.stockname: str = stockname
        self.input_width: int = input_width
        self.data: pd.core.frame.DataFrame = data
        self.output: pd.core.series.Series = output
        self.data_mean = self.data.mean()
        self.data_std = self.data.std()

        if(min_max):
            scaled_data, _, _ = self.normalize(
                self.data, data_std=self.data_std, data_mean=self.data_mean)  # TODO ? idk what the fuck to do with data mean and datastd
            self.scaled_data = self.min_max_scaler(scaled_data, -1., 1.)

    def make_windows(self, input_data: pd.core.frame.DataFrame, output_data: pd.core.series.Series = None, convert_to_numpy: bool = True):

        window_input = []
        if output_data is None:
            for i in range(self.input_width, len(input_data)):

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
                window_output.append(output_data[i])
                window_input[-1].pop("index")
                # convert pd.DataFrame to numpy
                window_input[-1] = window_input[-1].to_numpy()

            # convert list to numpy

            if(convert_to_numpy):
                window_input = np.asarray(window_input)
                window_output = np.asarray(window_output)

                window_output = tf.one_hot(window_output, depth=2)

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
