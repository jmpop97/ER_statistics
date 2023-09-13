import os
os.system('cls')

# 캐릭터 이름
'''
dic_characterNum_characterName[characterNum] = 캐릭터명
dic_characterNum_characterCount[characterNum] = 캐릭터별 빈도
dic_characterNum_BeforeMMR[characterNum]= {BeforeMMR:dic_BeforeMMR_datas}
dic_BeforeMMR_datas
=[{         
    "mmrGain": 얻은점수,
    "gameRank":게임 순위,
    "escapeState":탈출유무
 }]
'''
from read_txt import LoadCharacter
dic_characterNum_characterName=LoadCharacter()

#game_data 가져오기

import json
i=0
start_point=27619195
end_point=27621220
datas_num=start_point
dic_characterNum_characterCount={}
dic_characterNum_mmrBefore={}
while datas_num<end_point:
    datas_num=start_point+i
    with open(f"datas/{datas_num}.json", "r", encoding='utf-8') as f:
        game_datas = json.load(f)
    
    # 404 error
    if game_datas["code"]==404:
        i+=1
        continue
    
    # 일반제거
    game_type=game_datas["userGames"][0]["matchingMode"]
    if game_type==2 or game_type==6:
        i+=1
        continue

    for user_data in game_datas["userGames"]:
        '''유저 정보'''

        characterNum=user_data["characterNum"]
        mmrBefore=user_data["mmrBefore"]
        mmrGain=user_data["mmrGain"]
        gameRank=user_data["gameRank"]
        escapeState=user_data["escapeState"]
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("gameId",user_data["gameId"])
        print("gameRank",user_data["gameRank"])
        print("mmrBefore",user_data["mmrBefore"])
        print("teamKill",user_data["teamKill"])
        print("totalFieldKill",user_data["totalFieldKill"])
        print("mmrGain",user_data["mmrGain"])
        dic_characterNum_characterCount[characterNum]=dic_characterNum_characterCount.get(characterNum,0)+1
        if dic_characterNum_characterCount[characterNum]==1:
            dic_characterNum_mmrBefore[characterNum]={}
        mmrBefore_datas={
            "mmrGain": mmrGain,
            "gameRank":gameRank,
            "escapeState":escapeState
        }
        dic_characterNum_mmrBefore[characterNum][mmrBefore]= dic_characterNum_mmrBefore[characterNum].get(mmrBefore,[])+[mmrBefore_datas]
        # mmrBefore_mmrGain[mmrBefore]=mmrBefore_mmrGain.get(mmrBefore,[])+[mmrGain]
    i+=1
