import json
from datetime import datetime


with open("./model/settings.json", "r") as f:
    data: dict = json.load(f)


class ModelSettings():

    @staticmethod
    def save(param, param_name: str, data: dict = data):
        data[f"{param_name}"] = param

        with open("./model/settings.json", "w") as f:
            json.dump(data, f)

        if isinstance(model_settings.model_date, str):
            model_settings.model_date = datetime.strptime(
                model_settings.model_date, "%Y-%m-%d %H:%M:%S")

        if isinstance(model_settings.base_model_date, str):
            model_settings.base_model_date = datetime.strptime(
                model_settings.base_model_date, "%Y-%m-%d %H:%M:%S")


model_settings = ModelSettings()
for key, value in data.items():
    setattr(model_settings, key, value)

model_settings.model_date = datetime.strptime(
    model_settings.model_date, "%Y-%m-%d %H:%M:%S")
model_settings.base_model_date = datetime.strptime(
    model_settings.base_model_date, "%Y-%m-%d %H:%M:%S")
