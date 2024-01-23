import json
import os
from ER_apis.ER_api import save_games
from ER_apis.ER_api import game_api
from ER_datas.update_game_base_data import update_game_base_data
import sys

# Model
class Apimodel:
    def save_Api_key(self, key):
        api_key_dic = {"token": key}
        with open("setting\secret.json", "w") as file:
            json.dump(api_key_dic, file)

    def test_Api_key(self):
        if game_api:
            save_games(31460173, 1)
            return os.path.isfile("./datas/Ver10.0_Rank_31460173.json")
        else:
            return False


# View
class Apiview:
    @staticmethod
    def get_Api_key():
        if len(sys.argv)==2:
            return sys.argv[1]
        elif len(sys.argv)>2:
            print("다시 입력해주세요.")
            sys.exit()
        else:
            return input("키를 입력해주세요:")

    @staticmethod
    def show_result(result):
        print(result)


# Controller
class Apicontroller:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def get_api(self):
        if os.path.exists("setting") == False:
            os.mkdir("setting")

        while True:
            Api_key = self.view.get_Api_key()
            self.model.save_Api_key(Api_key)

            if self.model.test_Api_key():
                os.remove("./datas/Ver10.0_Rank_31460173.json")
                self.view.show_result("입력되었습니다.")
                break
            else:
                self.view.show_result("잘못된 키가 입력되었습니다.")
                sys.exit()

    def get_test_case(self):
        save_games(31131392, 1)
        save_games(31130633, 1)

    def make_main_py(self):
        main=open('main.py', 'w')
        main.close()

update_game_base_data()
model = Apimodel()
view = Apiview()
controller = Apicontroller(model, view)
controller.get_api()
controller.get_test_case()
controller.make_main_py()
