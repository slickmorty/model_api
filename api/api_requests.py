import json
import pandas as pd
import requests
from api.settings import api_settings


def delete_all() -> requests.Response:

    url = api_settings.delete_many
    payload = json.dumps({
        "collection": api_settings.collection,
        "database": api_settings.database,
        "dataSource": api_settings.data_source,
        "filter": {}
    })
    headers = {
        "Content-Type": api_settings.content_type,
        "Access-Control-Request-Headers": api_settings.access_control_request_headers,
        "api-key": api_settings.api_key
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    return response


def insert_all(df: pd.DataFrame) -> requests.Response:

    url = api_settings.insert_many
    records = df.to_dict("records")

    payload = json.dumps({
        "collection": api_settings.collection,
        "database": api_settings.database,
        "dataSource": api_settings.data_source,
        "documents": records
    })
    headers = {
        "Content-Type": api_settings.content_type,
        "Access-Control-Request-Headers": api_settings.access_control_request_headers,
        "api-key": api_settings.api_key
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    return response


def insert_one(df: pd.DataFrame) -> requests.Response:

    if(len(df) > 1):
        return
    url = api_settings.insert_one
    payload = json.dumps({
        "collection": api_settings.collection,
        "database": api_settings.database,
        "dataSource": api_settings.data_source,
        "document": df.to_dict("records")[0]
    })
    headers = {
        "Content-Type": api_settings.content_type,
        "Access-Control-Request-Headers": api_settings.access_control_request_headers,
        "api-key": api_settings.api_key
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    return response
