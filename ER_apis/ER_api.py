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

Views = ViewDownLoading()
load_dotenv()
OK_RESPONSE = int(os.environ.get("OK_RESPONSE", 0))
SEASON_ID = int(os.environ.get("SEASON_ID", 0))


def setting_header(param_dict: dict = {}) -> (dict, dict):
    with open("setting/secret.json", "r", encoding="utf-8") as f:
        token = json.load(f)
    header_dict = {}
    header_dict.setdefault("x-api-key", token["token"])
    return header_dict, param_dict


# translate string list to integer list
# ["Normal", "Normal", "Cobalt"] -> [2, 3, 6]
def translate_game_mode_str_to_int(input_game_mode_list: list) -> list:
    game_mode_num_list = []
    for game_mode in input_game_mode_list:
        if game_mode == "Normal":
            game_mode_num_list.append(NORMAL_MODE_NUMBER)
        elif game_mode == "Rank":
            game_mode_num_list.append(RANK_MODE_NUMBER)
        elif game_mode == "Cobalt":
            game_mode_num_list.append(COBALT_MODE_NUMBER)
    return game_mode_num_list


# translate integer list to String list
# [2, 3, 6] -> ["Normal", "Normal", "Cobalt"]
def translate_game_mode_int_to_str(input_game_mode_list: list) -> list:
    game_mode_num_list = []
    for game_mode in input_game_mode_list:
        if game_mode == NORMAL_MODE_NUMBER:
            game_mode_num_list.append("Normal")
        elif game_mode == RANK_MODE_NUMBER:
            game_mode_num_list.append("Rank")
        elif game_mode == COBALT_MODE_NUMBER:
            game_mode_num_list.append("Cobalt")
    return game_mode_num_list


# request api datas
def request_to_ER_api(
    request_url: str, header_dict: dict = None, second: int = 1
) -> dict:
    if header_dict == None:
        header_dict, _ = setting_header()
    try:
        requestDataWithHeader = requests.get(request_url, headers=header_dict)

        if requestDataWithHeader.status_code == OK_RESPONSE:
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


def game_api(game_id: int, str_game_type_list: list) -> bool:
    integer_game_type_list = translate_game_mode_str_to_int(str_game_type_list)

    responced_game_match_data = request_to_ER_api(
        request_url=f"https://open-api.bser.io/v1/games/{game_id}"
    )
    if not responced_game_match_data.get("userGames"):
        return False
    else:
        mode = responced_game_match_data["userGames"][0]["matchingMode"]
        if mode in integer_game_type_list:
            _save_game(game_id, responced_game_match_data)
        return True


def _save_game(game_id: int, responce_datas: dict) -> None:
    user_data = responce_datas["userGames"][0]
    game_major_version = user_data["versionMajor"]
    game_minor_version = user_data["versionMinor"]
    """ game_mode
    2 normal
    3 rank
    6 cobalt
    """
    game_mode = "Normal"
    if user_data["matchingMode"] == RANK_MODE_NUMBER:
        game_mode = "Rank"
    elif user_data["matchingMode"] == COBALT_MODE_NUMBER:
        game_mode = "Cobalt"
    """
    이거 서버도 여러개다.(Ohio, Seoul, SaoPaulo)
    """
    file_name = "./datas/Ver{0}.{1}_{2}_{3}.json".format(
        game_major_version, game_minor_version, game_mode, game_id
    )
    Views.file_name(file_name)
    with open(file_name, "w", encoding="utf-8") as outfile:
        json.dump(responce_datas, outfile, indent="\t", ensure_ascii=False)


def save_games(
    start_game: int,
    n: int = 1,
    second: int = 1,
    game_type: list = ["Rank", "Normal", "Cobalt"],
) -> bool:
    Views.end = n
    bool_value = True
    game_id = start_game
    while game_id < start_game + n:
        Views.start(game_id)
        Views.display()
        bool_value = game_api(game_id, game_type)
        if not bool_value:
            Views.bug()
        game_id += 1
        time.sleep(second)
    Views.start("end")
    Views.display()
    return bool_value


# def request_free_characters(matchingMode: str = NORMAL_MODE_NUMBER) -> bool:
#     responced_datas = request_to_ER_api(
#         request_url=f"https://open-api.bser.io/v1/freeCharacters/{matchingMode}"
#     )
#     if responced_datas.get("code", 0) != OK_RESPONSE:
#         return False
#     return True

# def request_top_players(seasonId:str=SEASON_ID, matchingTeamMode:str=RANK_MODE_NUMBER) -> dict | None:
#     responced_datas = request_to_ER_api(
#         request_url=f"https://open-api.bser.io/v1/rank/top/{seasonId}/{matchingTeamMode}"
#     )
#     if responced_datas.get("code", 0)!=OK_RESPONSE:
#         return None
#     return responced_datas


# language, ServerName
# 1. Korean, Seoul
# 2. ChineseSimplified, Seoul
# 3. English, Ohio
# 4. English,
# def request_region_rankers_eternity_cut(
#     seasonId: str = SEASON_ID,
#     matchingTeamMode: str = RANK_MODE_NUMBER,
#     region: str = "KR",
# ) -> dict | None:
#     responced_top_ranker_datas = request_top_players(seasonId, matchingTeamMode)
#     if responced_top_ranker_datas == None:
#         return None
#     ranker_datas = {
#         responced_top_ranker_data["nickname"]: {
#             "userNum": responced_top_ranker_data["userNum"],
#             "mmr": responced_top_ranker_data["mmr"],
#         }
#         for responced_top_ranker_data in responced_top_ranker_datas["topRanks"]
#     }
#     region_ranker_counter = 0
#     for ranker_nickname in ranker_datas.keys():
#         responced_top_ranker_datas = request_to_ER_api(
#             request_url=f"https://open-api.bser.io/v1/user/games/{ranker_datas[ranker_nickname]['userNum']}"
#         )
#         if responced_top_ranker_datas == None:
#             continue
#         if responced_top_ranker_datas["userGames"][0]["serverName"] == "Seoul":
#             region_ranker_counter += 1
#         if region_ranker_counter >= 200:
#             return {
#                 "date": datetime.today().strftime("%Y%m%d"),
#                 "mmr": ranker_datas[ranker_nickname]["mmr"],
#             }
#     return None


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
