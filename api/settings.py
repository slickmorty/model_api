import json


with open("./api/settings.json", "r") as f:
    data: dict = json.load(f)


class APISettings():
    @staticmethod
    def save(param, param_name: str, data: dict = data):
        data[f"{param_name}"] = param

        with open("./api/settings.json", "w") as f:
            json.dump(data, f)


api_settings = APISettings()

for key, value in data.items():
    setattr(api_settings, key, value)
