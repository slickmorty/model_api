import json
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
