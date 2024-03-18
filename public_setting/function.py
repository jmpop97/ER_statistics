import os
import dotenv
import re


def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print("Error: Creating directory. " + directory)


def createfile(name):
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
