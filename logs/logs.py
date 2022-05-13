import logging
import coloredlogs

GET_INITIAL_DATA = "Getting initial data from metatrader"
CONVERT_TO_CSV = "Saving initial data on CSV"
UPDATE_MODEL_INITIALLY = """
********************      UPDATING MODEL WITH DATA SINCE LAST TIME        ********************
********************              THIS COULD TAKE SOME TIME               ********************
********************          DON'T TOUCH THE KEYBOARD PLZ <3             ********************"""
FINISHED_UPDATING = "********Finished updating the model********"
LOADING = "LOADING..........."
PREDICTING = "Predicting"
GETTING_NEW_DATA = "Getting new data"
NEW_CANDLE_DETECTED = "New Candle Detected"
SAVING_CAREFULL = "********* Saving Data on disk, BE CAREFULL ***********"
WAITING_FOR_NEXT_CANDLE = "********* Waiting for next candle, At least 5 mins ***********"
DELETING_ALL_DATA = "********* Deleting all previous data in database ***********"
ADDING_NEW_DATA = "********* ADDING NEW DATA IN DATABASE ***********"
TRY_FAILED = "********* TRY FAILED *********"
UPDATING_MODEL = """
********************                  UPDATING_MODEL                      ********************
********************              THIS COULD TAKE SOME TIME               ********************
********************          DON'T TOUCH THE KEYBOARD PLZ <3             ********************"""

EXITING = """
********************                        EXITING                       ********************
********************                    HAVE A NICE DAY                   ********************"""


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
    logs.warning("""
    *****************************************************************************
    *****************************************************************************
    ********************    STARTING DON'T TOUCH KEYBOARD    ********************
    *****************************************************************************
    *****************************************************************************""")
