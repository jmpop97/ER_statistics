from ER1_mmr_datas import *
from mmr_range import Tier,getMMR_range,tier_range
from mmr_range import mmr_charges,mmr_line
from ER_datas.rank_mmr import rank_mmr

for i in characterNum_dic:
    globals()["range_num"+str(i)]=Tier()
    x=[]
    y=[]
    for mmrBefore in globals()["mmrBefore_datas"+str(i)]:
        for mmrBefore_datas in globals()["mmrBefore_datas"+str(i)][mmrBefore]:
            rankpoint,killpoint=rank_mmr(mmrBefore_datas["gameRank"])
            globals()["range_num"+str(i)].split_tier(mmrBefore,(mmrBefore_datas["mmrGain"]+mmr_charges(mmrBefore)-rankpoint-mmrBefore_datas["escapeState"]*10/3)/killpoint*4)

# 그래프

import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np

for num in characterNum_dic:
    plt.rcParams["font.family"] = 'Malgun Gothic'
    plt.style.use('_mpl-gallery')
    mpl.rcParams['axes.unicode_minus'] = False
    #캐릭터별
    plt.figure(num,figsize = (15, 8))
    plot_place=1
    # 티어별
    for tier_names in tier_range:
        tier_name=tier_range[tier_names]
        data = globals()["range_num"+str(num)].tier[tier_name]
        courses=[]
        values=[]
        for ranges in getMMR_range:
            courses += [getMMR_range[ranges]]
            values += [globals()["range_num"+str(num)].tier[tier_name].get(getMMR_range[ranges],0)]
        per_values=[]
        per_courses=[]
        sum_value = sum(values)
        if sum_value!=0:
            for i in values:
                per_values+=[i/sum_value]
            values=per_values
        # print(character_name[str(num)])
        # print(tier_name)
        # print(sum_value)
        # print(values)
            for i1,i2 in list(zip(courses,values)):
                per_courses+=[f'{i1}\n{i2:.2f}']
            courses=per_courses
    
        # creating the bar plot
        plt.subplot(3,3,plot_place)
        plt.bar(courses, values, color ='maroon',
                width = 0.4)
        plt.xlabel(f"get mmr ({sum_value})")
        plt.ylabel(tier_name+"%")
        plot_place+=1
        if plot_place==3:
            plt.title(character_name[str(num)],pad=10)
        plt.ylim([0,1])
    plt.subplots_adjust(left=0.07,bottom=0.07,top=0.9)
    plt.savefig("fig/"+character_name[str(num)]+"mmr_mmrGain_rank_range")
    plt.cla()   # clear the current axes
    plt.clf()   # clear the current figure
    plt.close() # closes the current figure
