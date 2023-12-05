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


def game_api(game_id):
    requestDataWithHeader = requests.get(
        f"https://open-api.bser.io/v1/games/{game_id}", headers=headerDict
    )
    responce_datas = requestDataWithHeader.json()
    save_game(game_id, responce_datas)


def save_game(game_id, responce_datas):
    with open(f"./datas/{game_id}.json", "w", encoding="utf-8") as outfile:
        json.dump(responce_datas, outfile, indent="\t", ensure_ascii=False)


def save_games(start_game, n=1, second=1):
    game_id = start_game
    while game_id < start_game + n:
        game_api(game_id)
        print(game_id)
        game_id += 1
        time.sleep(second)
    print("end")