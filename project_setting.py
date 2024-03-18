from public_setting.function import createfile, ENV
from ER_apis.ER_api import ERAPI_BASE_DB
from ER_datas.update_game_base_data import BaseDB


class View:
    def __init__(self):
        self.bug = {}

    def eternal_token(self):
        print("if 1 : skip")

        if self.bug:
            print(self.bug)

    def db_dir(self):
        print("game DB 저장할 폴더를 정해주세요")


class Controller:
    def eternal_token(self):
        return input("Eternal Return Token : ")

    def db_dir(self):
        return input("dir : ")


class Model:
    def __init__(self) -> None:
        self.con = Controller()
        self.view = View()
        self.env = ENV()
        # self.create_main()
        # self.set_token_get_origin_data()
        # self.setting_base_datas()
        self.db_dir()

    def set_token_get_origin_data(self) -> bool:
        while True:
            self.view.eternal_token()
            token = self.con.eternal_token()
            if token == "1":
                return True
            if ERAPI_BASE_DB().save_updated_game_base_data(token=token):
                self.env.put({"ER_TOKEN": token})
                return True
            self.view.bug = {"message": "잘못된 token값"}

    def setting_base_datas(self):
        BaseDB()

    def create_main(self):
        createfile("main.py")

    def db_dir(self):
        self.view.db_dir()
        dir = self.con.db_dir()
        self.env.put({"DB_DIR": dir})


Model()
