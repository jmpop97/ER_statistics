rank_point_dic={1:40,2:25,3:20,4:10,5:5,6:5,7:0,8:0}
#랭킹점수
rank_killpoint_dic={1:4,2:4,3:4,4:3,5:3,6:3,7:2,8:2}
def rank_mmr(rank):
    return rank_point_dic[rank],rank_killpoint_dic[rank]

#입장료
def mmr_charges(mmr):
    if mmr<1000:
        mmr_charge=0
    elif mmr<5000:
        mmr_charge=int(mmr/250)*2+2
    else:
        mmr_charge=int(mmr/250)*3-17
    return mmr_charge

#입량료 그래프 데이터
def mmr_line():
    figure_red={}
    mmr_range=[]
    mmr_charge_range=[]
    i=0
    while i<10000:
        mmr_range+=[i]
        mmr_charge_range+=[mmr_charges(i)]
        i+=250
        mmr_range+=[i]
        mmr_charge_range+=[mmr_charges(i-1)]
    figure_red["mmrBefore"]=mmr_range
    figure_red["mmrGain"]=mmr_charge_range
    return figure_red