import requests
import json
import os
import time

# Setting Header
with open("secret.json", "r", encoding='utf-8') as f:
    token = json.load(f)
headerDict = {}
headerDict.setdefault('x-api-key', token["token"])
paramDict = {}

def game_api(game_id): 
    requestDataWithHeader = requests.get(
        f'https://open-api.bser.io/v1/games/{game_id}', headers=headerDict)
    responce_datas = requestDataWithHeader.json()
    time.sleep(1)
    save_game(game_id,responce_datas)
    return True

def save_game(game_id,responce_datas):
    user_data = responce_datas['userGames'][0]
    game_major_version = user_data['versionMajor']
    game_minor_version=user_data["versionMinor"]
    game_mode="Normal"
    if user_data['matchingMode']==3:
        game_mode= "Rank"
    file_name = "./datas/Ver{0}.{1}_{2}_{3}.json".format(game_major_version, game_minor_version, game_mode, game_id)
    print(file_name)
    with open(file_name,'w',encoding='utf-8') as outfile:
        json.dump(responce_datas,outfile, indent="\t",ensure_ascii=False)

def save_games(start_game,n):
    game_id=start_game
    while game_id<start_game+n:
        if game_api(game_id)==True:
            print("saved", game_id)
            game_id+=1
    print("end")