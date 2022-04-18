import json
from datetime import datetime

with open("./model/settings.json", "r") as f:
    data: dict = json.load(f)

model_date: datetime = datetime.strptime(
    data.get("model_date"), "%Y-%m-%d %H:%M:%S")
base_model_date: str = data.get("base_model_date")
model_path: str = data.get("model_path")
base_model_path: str = data.get("base_model_path")
epoches: int = data.get("epoches")
loss: str = data.get("loss")
optimizer: str = data.get("optimizer")
batch_size: int = data.get("batch_size")


def save(param, param_name: str, data: dict = data):
    data[f"{param_name}"] = param

    with open("./model/settings.json", "w") as f:
        json.dump(data, f)
