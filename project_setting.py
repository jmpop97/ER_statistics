from public_setting.function import createFolder, createfile, ENV
from ER_apis.ER_api import ERAPI_BASE_DB
from ER_datas.update_game_base_data import BaseDB
import json
import sys
import os


class View:
    def __init__(self):
        self.DB = {}

    def eternal_token(self):
        print("if 1 : skip")

        if self.DB.get("bug"):
            print(self.DB["bug"])

    def db_dir(self):
        print("game DB 저장할 폴더를 정해주세요")

    def set_game_ver_major(self):
        print("major : int")

    def set_game_ver_minor(self):
        print("major : " + self.DB["major"])
        print("minor : int")


class Controller:
    def __init__(self, types) -> None:
        self.types = types

    def eternal_token(self):
        if self.types:
            return os.environ.get("ER_TOKEN")
        return input("Eternal Return Token : ")

    def db_dir(self):
        if self.types:
            return ""
        return input("dir : ")

    def set_game_ver_major(self):
        if self.types:
            return "15"
        return input("major : ")

    def set_game_ver_minor(self):
        if self.types:
            return "1"
        return input("minor : ")


class Model:
    def __init__(self, types: int = 0) -> None:
        self.con = Controller(types)
        self.view = View()
        self.env = ENV()

        self.set_token_get_origin_data()
        self.setting_base_datas()
        self.db_dir()
        self.set_game_ver()

    def set_token_get_origin_data(self) -> bool:
        while True:
            self.view.eternal_token()
            token = self.con.eternal_token()
            if token == "1":
                return True
            if ERAPI_BASE_DB().save_updated_game_base_data(token=token):
                self.env.put({"ER_TOKEN": token})
                return True
            self.view.DB["bug"] = {"message": "잘못된 token값"}

    def setting_base_datas(self):
        BaseDB()

    def create_main(self):
        createfile("main.py")

    def db_dir(self):
        self.view.db_dir()
        dir = self.con.db_dir()
        self.env.put({"DB_DIR": dir})

    def set_game_ver(self):
        self.view.set_game_ver_major()
        major = self.con.set_game_ver_major()
        self.view.DB["major"] = major
        self.view.set_game_ver_minor()
        minor = self.con.set_game_ver_minor()
        data = {
            "CURRENT_GAME_MAJOR_VERSION": major,
            "CURRENT_GAME_MINOR_VERSION": minor,
        }
        createFolder("./setting")
        with open("./setting/game_version.json", "w") as make_file:
            json.dump(data, make_file)


types = len(sys.argv) - 1
Model(types)
