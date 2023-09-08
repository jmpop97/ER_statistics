import os
os.system('cls')

# 캐릭터 이름
from read_txt import LoadCharacter
character_name=LoadCharacter()

#game_data 가져오기
'''characterNum_dic={캐릭터별 빈도}
"mmrBefore_datas{캐릭터번호}[beforeMMR]
=[{         
    "mmrGain": 얻은점수,
    "gameRank":게임 순위,
    "escapeState":탈출유무
 }]
'''
import json
i=0
characterNum_dic={}
while i<1000:
    datas_num=27233969+i
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
        characterNum_dic[characterNum]=characterNum_dic.get(characterNum,0)+1
        if characterNum_dic[characterNum]==1:
            globals()["mmrBefore_datas"+str(characterNum)]={}
        mmrBefore_datas={
            "mmrGain": mmrGain,
            "gameRank":gameRank,
            "escapeState":escapeState
        }
        globals()["mmrBefore_datas"+str(characterNum)][mmrBefore]=globals()["mmrBefore_datas"+str(characterNum)].get(mmrBefore,[])+[mmrBefore_datas]
        # mmrBefore_mmrGain[mmrBefore]=mmrBefore_mmrGain.get(mmrBefore,[])+[mmrGain]
    i+=1


# print(mmrBefore_mmrGain)