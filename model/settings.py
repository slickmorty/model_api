import json
import data.settings as data_settings

with open("./model/settings.json", "r") as f:
    data: dict = json.load(f)

model_date = data.get("model").get("date")
model_path = data.get("model").get("model_path")
base_model_path = data.get("model").get("base_model_path")
epoches = data.get("model").get("epoches")
loss = data.get("model").get("loss")
optimizer = data.get("model").get("optimizer")
