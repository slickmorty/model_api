import json
import requests
from api import settings as api_settings

url = api_settings.delete_many

payload = json.dumps({
    "collection": api_settings.collection,
    "database": api_settings.database,
    "dataSource": api_settings.data_source,
    "filter": {}
})
headers = {
    "Content-Type": api_settings.content_type,
    "Access-Control-Request-Headers": api_settings.acrh,
    "api-key": api_settings.api_key
}

response = requests.request("POST", url, headers=headers, data=payload)
response.text
