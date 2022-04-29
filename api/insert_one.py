import pandas as pd
import requests
import json
from api.settings import api_settings


def insert_one(df: pd.DataFrame) -> requests.Response:

    if(len(df) > 1):
        return
    url = api_settings.insert_one

    payload = json.dumps({
        "collection": api_settings.collection,
        "database": api_settings.database,
        "dataSource": api_settings.data_source,
        "documents": df.to_dict("records")
    })
    headers = {
        "Content-Type": api_settings.content_type,
        "Access-Control-Request-Headers": api_settings.access_control_request_headers,
        "api-key": api_settings.api_key
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    return response
