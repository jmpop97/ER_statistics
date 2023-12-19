# save api datas
# from ER_apis.ER_api import save_games

# save_games(30784252,10)
# sort data
from ER_datas.ERDataCleansing import ERDataCleansing
from ER_datas.data_class import *
from ER_fig.figure_datas import FigureType

dic_name = {"10*gameRank": "gameRank10"}
data_class = ListFilterData(
    "playTime", "mmrGainInGame", "gameRank", "10*gameRank", **dic_name
)
ERDataCleansing(data_class=data_class)
print(len(data_class.conditions["mmrGainInGame"]))
print(len(data_class.conditions["playTime"]))
# figure
from ER_fig.figure_datas import FigureType

test = FigureType()
test.scatterplot(
    data_class.conditions,
    "playTime",
    "mmrGainInGame",
    titles="",
    team_color="red",
    figure_n=1,
)
test.scatterplot(
    data_class.conditions,
    "playTime",
    "gameRank10",
    titles="",
    team_color="red",
    figure_n=2,
)
test.save_show()
# test.barplot(data=data_class.conditions,x="playTime",y="gameRank",figure_n=1)
# test.barplot(data=data_class.conditions,x="playTime",y="mmrGainInGame",figure_n=2)
# test.save_show()


character_console_class = CharacterClass("")
print(ERDataCleansing(character_console_class, ["Rank", "Normal"]))
print(character_console_class.get_data())

"""0
data_class=FilterData("mmrBefore","mmrGain")
ERDataCleansing(data_class=data_class)
print(data_class.dic_characterNum_datas)
0"""
"""example ForeignTeam class"""
# #sort datas
# data_class=ForeignTeam("mmrBefore","mmrGainInGame","gameRank")
# ERDataCleansing(30306839,30306839+1000,data_class)
# print(data_class.team["domestic_team"]["tier"].tier["all"])

# #figure
# # sort data
# from ER_datas.ERDataCleansing import ERDataCleansing
# from ER_datas.data_class import *
# from ER_fig.figure_datas import FigureType

# """example FilterData class"""
# """0
# data_class=FilterData("mmrBefore","mmrGain")
# ERDataCleansing(data_class=data_class)
# print(data_class.dic_characterNum_datas)
# 0"""
# """example ForeignTeam class"""
# # #sort datas
# # data_class=ForeignTeam("mmrBefore","mmrGainInGame","gameRank")
# # ERDataCleansing(30306839,30306839+1000,data_class)
# # print(data_class.team["domestic_team"]["tier"].tier["all"])

# # #figure
# # from ER_fig.figure_datas import FigureType
# # test=FigureType()
# # # test.scatterplot(data_class.team["domestic_team"],"mmrGainInGame","mmrBefore",titles="domestic_team",team_color="blue",figure_n=1)
# # # test.scatterplot(data_class.team["foreigner_team"],"mmrGainInGame","mmrBefore",titles="foreign_team",team_color="red",figure_n=1)
# # for tier_name in data_class.team["domestic_team"]["tier"].tier:
# #     test.bar_graph(data_class.team["domestic_team"]["tier"].tier[tier_name],bar_count=2,bar_num=1,team_color="blue",figure_n=tier_name)
# #     test.bar_graph(data_class.team["foreigner_team"]["tier"].tier[tier_name],bar_count=2,bar_num=2,team_color="red",figure_n=tier_name)

# # test.show()

# data_calss = Camera_All(
#     "mmrBefore",
#     "mmrGainIngame",
#     "addSurveillanceCamera",
#     "addTelephotoCamera",
#     "gameRank",
#     "characterNum",
# )
# ERDataCleansing(data_calss)
# test = FigureType()
# test.bar_graph_all(
#     data_calss.dic_cameraGroup_mmr,
#     data_calss.dic_cameraGroup_tier,
#     data_calss.dic_cameraGroup_Rank,
#     data_calss.dic_cameraGroup_LukeMai,
# )
# test.show()
# # import pprint

# # emoticon_class = EmoticonMMRClass(split_range=1000)
# # pprint.pprint(ERDataCleansing(30386977, 30386977, emoticon_class))

# """
# #figure
# # from ER_fig.figure_datas import figure_save
# # figure_type="range_split_mmr"
# # list_request_datatype=["mmrBefore","mmrGain"]
# # # figure_save(dic_characterNum_datas,figure_type,list_request_datatype)
# 2 """
