import requests
import json
import os
import time

# Setting Header
with open("secret.json", "r", encoding="utf-8") as f:
    token = json.load(f)
headerDict = {}
headerDict.setdefault("x-api-key", token["token"])
paramDict = {}


def game_api(game_id, str_game_type_list):
    game_type_list = []
    for game_type in str_game_type_list:
        if game_type == "Normal":
            game_type_list.append(2)
        elif game_type == "Rank":
            game_type_list.append(2)
        elif game_type == "Cobalt":
            game_type_list.append(6)
    requestDataWithHeader = requests.get(
        f"https://open-api.bser.io/v1/games/{game_id}", headers=headerDict
    )
    responce_datas = requestDataWithHeader.json()
    time.sleep(1)
    if responce_datas.get("code", 0) == 200:
        mode = responce_datas["userGames"][0]["matchingMode"]
        if mode in game_type_list:
            save_game(game_id, responce_datas)
    return True


def save_game(game_id, responce_datas):
    user_data = responce_datas["userGames"][0]
    game_major_version = user_data["versionMajor"]
    game_minor_version = user_data["versionMinor"]
    game_mode = "Normal"
    # 2 normal
    # 3 rank
    # 6 cobalt
    """
    이거 서버도 여러개다.(Ohio, Seoul, SaoPaulo)
    """
    if user_data["matchingMode"] == 3:
        game_mode = "Rank"
    elif user_data["matchingMode"] == 6:
        game_mode = "Cobalt"
    file_name = "./datas/Ver{0}.{1}_{2}_{3}.json".format(
        game_major_version, game_minor_version, game_mode, game_id
    )
    print(file_name)
    with open(file_name, "w", encoding="utf-8") as outfile:
        json.dump(responce_datas, outfile, indent="\t", ensure_ascii=False)


def save_games(start_game, n=1, second=1, game_type=["Rank"]):
    game_id = start_game
    while game_id < start_game + n:
        game_api(game_id, game_type)
        print("game_id: ", game_id, "({0}/{1})".format(game_id - start_game + 1, n))
        game_id += 1
        time.sleep(second)
    print("end")
