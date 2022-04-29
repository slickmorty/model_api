import json


with open("./data/settings.json", "r") as f:
    data: dict = json.load(f)


class DataSettings():

    @staticmethod
    def save(param, param_name: str, data: dict = data):
        data[f"{param_name}"] = param

        with open("./data/settings.json", "w") as f:
            json.dump(data, f)


data_settings = DataSettings()


for key, value in data.items():
    setattr(data_settings, key, value)
