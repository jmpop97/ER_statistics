import requests
import json
import os
import time
os.system('cls')

with open("secret.json", "r", encoding='utf-8') as f:
    token = json.load(f)


# Setting Header
headerDict = {}
headerDict.setdefault('x-api-key', token["token"])
paramDict = {}

# Request
game_id=27233969
while(True):
    i=0
    game_id+=1
    requestDataWithHeader = requests.get(
        f'https://open-api.bser.io/v1/games/{game_id}', headers=headerDict)
    responce_datas = requestDataWithHeader.json()
    with open(f"{game_id}.json",'w',encoding='utf-8') as outfile:
        json.dump(responce_datas,outfile, indent="\t",ensure_ascii=False)
    if i==1000:
        break
    time.sleep(1)
# with open("27233969.json", "r",encoding='utf-8') as json_file:
#     json_data = json.load(json_file)
#     print(json_data)