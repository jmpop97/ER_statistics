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
start_game_id=27721407
end_point=2
# end_game_id=27620198
end_game_id=start_game_id+end_point-1
while(True):

    #api요청
    requestDataWithHeader = requests.get(
        f'https://open-api.bser.io/v1/games/{start_game_id}', headers=headerDict)
    responce_datas = requestDataWithHeader.json()
    
    #api저장
    with open(f"datas/{start_game_id}.json",'w',encoding='utf-8') as outfile:
        json.dump(responce_datas,outfile, indent="\t",ensure_ascii=False)

    #갯수 제한
    if start_game_id==end_game_id:
        break
    time.sleep(1)
    start_game_id+=1
print("end")
# with open("27233969.json", "r",encoding='utf-8') as json_file:
#     json_data = json.load(json_file)
#     print(json_data)