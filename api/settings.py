import json


with open("./api/settings.json", "r") as f:
    data: dict = json.load(f)

api_key: str = data.get("api-key")
collection: str = data.get("collection")
database: str = data.get("database")
data_source: str = data.get("dataSource")
content_type: str = data.get("Content-Type")
acrh: str = data.get("Access-Control-Request-Headers")

insert_one: str = data.get("insertOne")
insert_many: str = data.get("insertMany")
delete_many: str = data.get("deleteMany")


def save(param, param_name: str, data: dict = data):
    data[f"{param_name}"] = param

    with open("./data/settings.json", "w") as f:
        json.dump(data, f)
# : str = data.get("")
