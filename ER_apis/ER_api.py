import requests
import json
from View.View import ViewDownLoading
import time
from datetime import datetime
import os
from dotenv import load_dotenv
from glob import glob
import re
from public_setting.variable import GameDB, GameType
from public_setting.function import createFolder, createfile, ENV

load_dotenv()


def setting_header(param_dict: dict = {}) -> (dict, dict):
    with open("setting/secret.json", "r", encoding="utf-8") as f:
        token = json.load(f)
    header_dict = {}
    header_dict.setdefault("x-api-key", token["token"])
    return header_dict, param_dict

def request_to_ER_api(
    request_url: str, header_dict: dict = None, second: int = 1
) -> dict:
    if header_dict == None:
        header_dict, _ = setting_header()
    try:
        requestDataWithHeader = requests.get(request_url, headers=header_dict)

        if requestDataWithHeader.status_code == "200":
            responced_datas = requestDataWithHeader.json()
            return responced_datas
        elif requestDataWithHeader.status_code == 429:
            print("Too many requests. Waiting and retrying...")
            time.sleep(second)
            return request_to_ER_api(request_url, header_dict, second)
        else:
            print("Error: {0}".format(requestDataWithHeader.status_code))
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def request_to_ER_api(
    request_url: str, header_dict: dict = None, second: int = 1
) -> dict:
    if header_dict == None:
        header_dict, _ = setting_header()
    try:
        requestDataWithHeader = requests.get(request_url, headers=header_dict)

        if requestDataWithHeader.status_code == "200":
            responced_datas = requestDataWithHeader.json()
            return responced_datas
        elif requestDataWithHeader.status_code == 429:
            print("Too many requests. Waiting and retrying...")
            time.sleep(second)
            return request_to_ER_api(request_url, header_dict, second)
        else:
            print("Error: {0}".format(requestDataWithHeader.status_code))
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None


class ERAPI:
    def __init__(self):
        self.game_type = ["Rank", "Normal", "Cobalt"]
        self.game_id = 0
        self.View = ViewDownLoading()
        self.type_dic = GameType()

    def open_dir_file(self):
        file_dir = self.root_dir + "/*"
        file_list = glob(file_dir)
        self.game_list = [re.split("[_.]", file)[-2] for file in file_list]

    def save_games(
        self,
        start_game: int,
        n: int = 1,
        second: int = 1,
        game_type: list = ["Rank", "Normal", "Cobalt"],
        duplication: bool = True,
        reverse: bool = True,
        d: int = 1,
        root_dir: str = os.environ.get("DB_DIR", "./datas"),
    ) -> bool:
        self.game_id = start_game
        self.View.end = n
        self.game_type = game_type
        self.game_list = GameDB(root_dir=root_dir).game_list
        self.root_dir = root_dir
        createFolder(root_dir)
        reverse_n = -1 if reverse else 1

        while self.View.count < self.View.end - 1:
            self.View.start(self.game_id)
            self.View.display()
            if duplication:
                if str(self.game_id) in self.game_list:
                    self.View.duplication_skip(self.game_id)
                    self.game_id += reverse_n * d
                    continue
            if not self.game_api():
                self.View.bug()
            self.game_id += reverse_n * d
            time.sleep(second)
        self.View.start("end")
        self.View.display()
        return not bool(self.View.bug_memory)

    def game_api(self) -> bool:
        responced_game_match_data = self.request_to_ER_api(
            request_url=f"https://open-api.bser.io/v1/games/{self.game_id}"
        )

        if not responced_game_match_data.get("userGames"):
            return False
        else:
            mode = responced_game_match_data["userGames"][0]["matchingMode"]
            if self.type_dic.num_type.get(mode, 0):
                self._save_game(responced_game_match_data)
            else:
                self.View.type_skip(self.game_id)
            return True

    def _save_game(self, responce_datas: dict) -> None:
        user_data = responce_datas["userGames"][0]
        game_major_version = user_data["versionMajor"]
        game_minor_version = user_data["versionMinor"]

        game_mode = self.type_dic.num_type.get(user_data["matchingMode"], "Bug")
        """
        이거 서버도 여러개다.(Ohio, Seoul, SaoPaulo)
        """
        file_name = self.root_dir + "/Ver{0}.{1}_{2}_{3}.json".format(
            game_major_version, game_minor_version, game_mode, self.game_id
        )
        print(file_name)
        self.View.file_name(file_name)
        with open(file_name, "w", encoding="utf-8") as outfile:
            json.dump(responce_datas, outfile, indent="\t", ensure_ascii=False)

    def request_to_ER_api(
        self, request_url: str, header_dict: dict = None, second: int = 1
    ) -> dict:
        if header_dict == None:
            header_dict, _ = self.setting_header()
        try:
            requestDataWithHeader = requests.get(request_url, headers=header_dict)
            if requestDataWithHeader.status_code == 200:
                responced_datas = requestDataWithHeader.json()
                return responced_datas
            elif requestDataWithHeader.status_code == 429:
                print("Too many requests. Waiting and retrying...")
                time.sleep(second)
                return self.request_to_ER_api(request_url, header_dict, second)
            else:
                print("Error: {0}".format(requestDataWithHeader.status_code))
                return None
        except Exception as e:
            print(f"Error: {e}")
            return None

    def setting_header(self, param_dict: dict = {}) -> (dict, dict):
        token = os.environ.get("ER_TOKEN")
        header_dict = {}
        header_dict.setdefault("x-api-key", token)
        return header_dict, param_dict


class ERAPI_BASE_DB:
    def __init__(self) -> None:
        self.path = "./origin_datas/"
        self.txt_name = "game_base_data.txt"

    def save_updated_game_base_data(self, token, language="Korean"):
        url = "https://open-api.bser.io/v1/l10n/Korean/"
        datas = {"x-api-key": token, "language": language}
        response = requests.get(url, headers=datas)
        response_datas = response.json()
        print(response_datas)
        if response_datas.get("code", 0) == 200:
            file_url = response_datas["data"]["l10Path"]
            file = requests.get(file_url)
            txt_path = self.path + self.txt_name
            createFolder(self.path)
            createfile(txt_path)
            env_data = {
                "BASE_DATAS_PATH": self.path,
                "TXT_GAME_BASE_DATA_FILE_NAME": self.txt_name,
            }

            ENV().put(env_data)
            open(txt_path, "wb").write(file.content)
            return True
        else:
            return False
