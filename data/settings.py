import json


with open("data/setting.json", "r") as f:
    data = json.load(f)

print(data["data"]["symbol"])
