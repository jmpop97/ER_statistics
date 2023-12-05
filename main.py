# save api datas
from ER_apis.ER_api import save_games

# save_games(30780251,4000)

# sort data
from ER_datas.ERDataCleansing import ERDataCleansing
from ER_datas.data_class import *

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


""" 2
character_console_class=CharacterClass("")
print(ERDataCleansing(character_console_class, ["Rank", "Normal"]))
print(character_console_class.get_data())
'''
import pprint
emoticon_class=EmoticonMMRClass(split_range=1000)
pprint.pprint(ERDataCleansing(30386977,30386977,emoticon_class))
'''
'''
#figure 
# from ER_fig.figure_datas import figure_save
# figure_type="range_split_mmr"
# list_request_datatype=["mmrBefore","mmrGain"]
# # figure_save(dic_characterNum_datas,figure_type,list_request_datatype)
2 """
