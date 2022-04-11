import json
import data.settings as data_settings

with open("./model/settings.json", "r") as f:
    data: dict = json.load(f)

model_name = data.get("model").get("name")

print(f"{model_name=}")
print(f"{data_settings.symbol=}")
