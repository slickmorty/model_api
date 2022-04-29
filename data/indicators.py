import datetime as dt
import pandas as pd
from data.settings import data_settings
import ta

future_window_size = data_settings.future_window_size


def add_indicators(df: pd.core.frame.DataFrame) -> pd.core.frame.DataFrame:
    """Adding indicators to the dataframe

    Args:
        df (pd.core.frame.DataFrame): dataframe

    Returns:
        df (pd.core.frame.DataFrame): dataframe
    """

    # MACD
    macd = ta.trend.MACD(df["Close"])
    df["MACD"] = macd.macd()
    df["MACD_Signal"] = macd.macd_signal()
    df["MACD_Diff"] = macd.macd_diff()

    # RSI
    rsi = ta.momentum.RSIIndicator(df["Close"])
    df["RSI"] = rsi.rsi()

    # CCI
    cci = ta.trend.CCIIndicator(
        high=df["High"], low=df["Low"], close=df["Close"])
    df["CCI"] = cci.cci()

    # STOCHASTIC
    stochastic = ta.momentum.StochasticOscillator(
        close=df["Close"], high=df["High"], low=df["Low"]
    )
    df["STOCH"] = stochastic.stoch()
    df["STOCH_SIGNAL"] = stochastic.stoch_signal()

    # BOLLINGER
    bollinger = ta.volatility.BollingerBands(close=df["Close"])
    df["Boll_Percent"] = bollinger.bollinger_pband()

    # WilliamsRIndicator
    williamsRIndicator = ta.momentum.WilliamsRIndicator(
        close=df["Close"], high=df["High"], low=df["Low"]
    )
    df["WILL_R"] = williamsRIndicator.williams_r()

    # DonchianChannel
    dcc = ta.volatility.DonchianChannel(
        high=df["High"], low=df["Low"], close=df["Close"]
    )
    df["DON_CHIAN_pband"] = dcc.donchian_channel_pband()

    # ADX
    adx = ta.trend.ADXIndicator(
        high=df["High"], low=df["Low"], close=df["Close"])
    df["ADX_Pos"] = adx.adx_pos()
    df["ADX_Neg"] = adx.adx_neg()

    # AROON
    aroon = ta.trend.AroonIndicator(close=df["Close"])
    df["Aroon"] = aroon.aroon_indicator()

    return df


def add_candles(df: pd.core.frame.DataFrame) -> pd.core.frame.DataFrame:
    """Making and adding candles to the dataframe

    Args:
        df (pd.core.frame.DataFrame): dataframe

    Returns:
        df (pd.core.frame.DataFrame): dataframe
    """

    # Calculating candel upper and lower shadow
    candel_upper_shadow = []
    candel_lower_shadow = []

    for i in range(len(df["Close"])):

        if df["Close"][i] > df["Open"][i]:
            candel_upper_shadow.append((df["High"][i] - df["Close"][i]))
        else:
            candel_upper_shadow.append((df["High"][i] - df["Open"][i]))

        if df["Close"][i] > df["Open"][i]:
            candel_lower_shadow.append((df["Open"][i] - df["Low"][i]))
        else:
            candel_lower_shadow.append((df["Close"][i] - df["Low"][i]))

    df["Candle_Upper_Shadow"] = candel_upper_shadow
    df["Candle_Body"] = df["Close"] - df["Open"]
    df["Candle_Lower_Shadow"] = candel_lower_shadow

    return df


def add_class(df: pd.DataFrame) -> pd.DataFrame:

    buy_or_sell_number = []

    def average(index: int, future_window_size: int):
        sum = 0.
        for i in range(index, index+future_window_size):
            sum += df['Close'][i+1]

        return sum/future_window_size

    # number_of_buys = 0
    # number_of_sells= 0
    for i in range(len(df['Close'])-future_window_size):
        if(average(i, future_window_size) > df['Close'][i]):
            buy_or_sell_number.append(1)
            # number_of_buys = number_of_buys+1
        else:
            buy_or_sell_number.append(0)
            # number_of_sells = number_of_sells+1

    for i in range(future_window_size):
        buy_or_sell_number.append(-1)

    df['Real'] = buy_or_sell_number
    return df
