rank_point_dic={1:40,2:25,3:20,4:10,5:5,6:5,7:0,8:0}
rank_killpoint_dic={1:4,2:4,3:4,4:3,5:3,6:3,7:2,8:2}
def rank_mmr(rank):
    return rank_point_dic[rank],rank_killpoint_dic[rank]

    