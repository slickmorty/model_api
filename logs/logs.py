import logging
import coloredlogs

GET_INITIAL_DATA = "Getting initial data from metatrader"
CONVERT_TO_CSV = "Saving initial data on CSV"
UPDATE_MODEL_INITIALLY = """
\t********************      UPDATING MODEL WITH DATA SINCE LAST TIME        ********************
\t********************              THIS COULD TAKE SOME TIME               ********************
\t********************          DON'T TOUCH THE KEYBOARD PLZ <3             ********************"""
FINISHED_UPDATING = "********Finished updating the model********"
LOADING = "LOADING..........."
PREDICTING = "Predicting"
GETTING_NEW_DATA = "Getting new data"
NEW_CANDLE_DETECTED = "New Candle Detected"
SAVING_CAREFULL = "********* Saving Data on disk, BE CAREFULL ***********"
WAITING_FOR_NEXT_CANDLE = "********* Waiting for next candle, At least 5 mins ***********"


def make_logs(logs):

    levelstyles = {'critical': {'bold': True, 'color': 'red'},
                   'debug': {'color': 'green'},
                   'error': {'color': 'red'},
                   'info': {'color': 'magenta'},
                   'warning': {'color': 'yellow'}}

    file = logging.FileHandler("./logs/model.log")
    file_format = logging.Formatter(
        '%(asctime)s %(levelname)s :%(message)s', datefmt='%m/%d/%Y %I:%M:%S %p',)
    file.setFormatter(file_format)
    logs.addHandler(file)

    coloredlogs.install(level=logging.INFO, logger=logs,
                        fmt='%(asctime)s %(levelname)s :%(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level_styles=levelstyles)


def start(logs):
    logs.warning(
        "\n\n\t********************\tSTARTING DON'T TOUCH KEYBOARD\t********************n\n")
