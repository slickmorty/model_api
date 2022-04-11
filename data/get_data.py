from datetime import datetime
import MetaTrader5 as mt5


def get_initial_data(model_date: str, symbol: str):

    model_date = datetime.strptime(model_date, "%y-%m-%d %H:%M:%S")
    if not mt5.initialize():
        print("initialize() failed")
        mt5.shutdown()

    data1 = mt5.copy_rates_range(
        symbol, mt5.TIMEFRAME_M5, model_date, datetime.now())

    data2 = mt5.copy_rates_from(symbol, mt5.TIMEFRAME_M5, model_date, 256)

    return data1, data2


def get_live_data():
    return


def load_data_from_csv():
    return


if __name__ == "__main__":

    model_name = "22-03-10 19:31:00"
    a, b = get_initial_data(model_name, "SP500m")
    print(len(b))
