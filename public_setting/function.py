import os
import dotenv
import json


def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print("Error: Creating directory. " + directory)


def createfile(name):
    _names = name
    _names = _names.split("/")
    if len(_names) >= 2:
        _names.pop()
        _names = "/".join(_names)
        createFolder(_names)
    try:
        with open(name, mode="r") as file:
            pass
    except:
        with open(name, mode="w") as file:
            pass


class ENV:
    def __init__(self) -> None:
        createfile(".env")
        self.dotenv_file = dotenv.find_dotenv()
        self.env = dotenv.load_dotenv(self.dotenv_file)

    def put(self, dic: dict):
        for key, value in dic.items():
            dotenv.set_key(self.dotenv_file, key, value, quote_mode="never")


class Json:
    def save(self, file_path, data):
        createfile(file_path)
        with open(file_path, "w") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    def read(self, file_path):
        try:
            with open(file_path, "r") as file:
                data = json.load(file)
        except:
            data = {400: "None File"}
        return data
