import os
os.system('cls')

# 캐릭터 이름
from read_txt import LoadCharacter
character_name=LoadCharacter()

#game_data 가져오기
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
            globals()["mmrBefore_mmrGain"+str(characterNum)]={}
        mmrBefore_datas={
            "mmrGain": mmrGain,
            "gameRank":gameRank,
            "escapeState":escapeState
        }
        globals()["mmrBefore_mmrGain"+str(characterNum)][mmrBefore]=globals()["mmrBefore_mmrGain"+str(characterNum)].get(mmrBefore,[])+[mmrBefore_datas]
        # mmrBefore_mmrGain[mmrBefore]=mmrBefore_mmrGain.get(mmrBefore,[])+[mmrGain]
    i+=1
# print(mmrBefore_mmrGain)

#통계분석
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np
plt.rcParams["font.family"] = 'Malgun Gothic'
plt.style.use('_mpl-gallery')
mpl.rcParams['axes.unicode_minus'] = False

characterNumber=len(characterNum_dic)

from mmr_range import mmr_charges,mmr_line
mmr_ranges,mmr_lines=mmr_line()



for i in characterNum_dic:
    x=[]
    y=[]
    for mmrBefore in globals()["mmrBefore_mmrGain"+str(i)]:
        for mmrBefore_datas in globals()["mmrBefore_mmrGain"+str(i)][mmrBefore]:
            x+=[mmrBefore]
            print()
            y+=[mmrBefore_datas["mmrGain"]+mmr_charges(mmrBefore)]



    # size and color:

    # plot
    plt.figure(i,figsize=(10,6))
    plt.plot(x, y,'o')
    plt.title(character_name[str(i)],pad=10)
    plt.xlabel('mmrBefore',labelpad=10)
    plt.ylabel('mmrGet',labelpad=10)
    plt.plot(mmr_ranges,mmr_lines,'r')
    plt.subplots_adjust(left=0.07,bottom=0.06,top=0.9)
    plt.savefig("fig/"+character_name[str(i)]+"mmr_mmrGain")

