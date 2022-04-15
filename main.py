from datetime import datetime

from certifi import where
from data import get_data, settings as data_settings, indicators, DataProcessing
from model import model_update, settings as model_settings
from logs import logs
import numpy as np
import pandas as pd
import time

import logging
mylogs = logging.getLogger(__name__)


def main():
    logs.start(mylogs)
    mylogs.info(logs.GET_INITIAL_DATA)
    data_until_now, data_before_model_date = get_data.get_initial_data()

    mylogs.info(logs.CONVERT_TO_CSV)
    df = get_data.get_initial_data_and_convert_to_pandas(
        data_until_now, data_before_model_date)

    mylogs.critical(logs.UPDATE_MODEL_INITIALLY)
    model, data = model_update.update_model_with_initial_info(df)

    # while(True):

    #     time.sleep(1)


if __name__ == "__main__":
    logs.make_logs(logs=mylogs)
    main()
