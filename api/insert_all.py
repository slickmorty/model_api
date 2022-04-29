import requests
import json
from api import settings as api_settings


url = api_settings.insert_many

payload = json.dumps({
    "collection": api_settings.collection,
    "database": api_settings.database,
    "dataSource": api_settings.data_source,
    "documents": df.to_dict("records")
})
headers = {
    "Content-Type": api_settings.content_type,
    "Access-Control-Request-Headers": api_settings.acrh,
    "api-key": api_settings.api_key
}

response = requests.request("POST", url, headers=headers, data=payload)
