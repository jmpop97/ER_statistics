import requests
import json
from function.public_function import clear_terminal
import time

NORMAL_MODE_NUMBER = 2
RANK_MODE_NUMBER = 3
COBALT_MODE_NUMBER = 6
OK_RESPONSE = 200
SEASON_ID = 21

# Setting Header
with open("setting/secret.json", "r", encoding="utf-8") as f:
    token = json.load(f)
headerDict = {}
headerDict.setdefault("x-api-key", token["token"])
paramDict = {}


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
def request_to_ER_api(request_url: str, header_dict: dict = None) -> dict:
    if header_dict == None:
        header_dict, _ = setting_header()
    requestDataWithHeader = requests.get(request_url, headers=header_dict)
    responced_datas = requestDataWithHeader.json()
    if responced_datas.get("code", 0) != OK_RESPONSE:
        responced_datas = None
    return responced_datas


def game_api(game_id: int, str_game_type_list: list) -> bool:
    integer_game_type_list = translate_game_mode_str_to_int(str_game_type_list)

    responced_game_match_data = request_to_ER_api(
        request_url=f"https://open-api.bser.io/v1/games/{game_id}"
    )
    if responced_game_match_data == None:
        return False
    else:
        mode = responced_game_match_data["userGames"][0]["matchingMode"]
        if mode in integer_game_type_list:
            _save_game(game_id, responced_game_match_data)



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
    if user_data["matchingMode"] == 3:
        game_mode = "Rank"
    elif user_data["matchingMode"] == 6:
        game_mode = "Cobalt"
    """
    이거 서버도 여러개다.(Ohio, Seoul, SaoPaulo)
    """
    file_name = "./datas/Ver{0}.{1}_{2}_{3}.json".format(
        game_major_version, game_minor_version, game_mode, game_id
    )
    print(file_name)
    with open(file_name, "w", encoding="utf-8") as outfile:
        json.dump(responce_datas, outfile, indent="\t", ensure_ascii=False)


def save_games(
    start_game: int,
    n: int = 1,
    second: int = 1,
    game_type: list = ["Rank", "Normal", "Cobalt"],
) -> bool:
    game_id = start_game
    while game_id < start_game + n:
        if not game_api(game_id, game_type):
            return False
        print("game_id: ", game_id, "({0}/{1})".format(game_id - start_game + 1, n))
        game_id += 1
        time.sleep(second)
        clear_terminal()
    print("end save_games")
    return True


def request_free_characters(matchingMode: str = NORMAL_MODE_NUMBER) -> bool:
    responced_datas = request_to_ER_api(
        request_url=f"https://open-api.bser.io/v1/freeCharacters/{matchingMode}"
    )
    if responced_datas.get("code", 0) != OK_RESPONSE:
        return False
    return True
