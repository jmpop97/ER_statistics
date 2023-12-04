# save api datas
from ER_apis.ER_api import save_games

# save_games(30780251,4000)

# sort data
from ER_datas.ERDataCleansing import ERDataCleansing
from ER_datas.data_class import *

30780683
"""example FilterData class"""
"""0
data_class=FilterData("mmrBefore","mmrGain")
ERDataCleansing(data_class=data_class)
print(data_class.dic_characterNum_datas)
0"""
"""example ForeignTeam class"""

# sort datas
data_class = ForeignTeam("mmrBefore", "mmrGainInGame", "gameRank")
ERDataCleansing(data_class=data_class)
# print("domestic_team", data_class.team["domestic_team"]["mmrBefore"])
# print("foreigner_team", data_class.team["foreigner_team"]["tier"].tier)

# figure
from ER_fig.figure_datas import FigureType

test = FigureType()
# test.scatterplot(data_class.team["domestic_team"],"mmrGainInGame","mmrBefore",titles="domestic_team",team_color="blue",figure_n=1)
# test.scatterplot(data_class.team["foreigner_team"],"mmrGainInGame","mmrBefore",titles="foreign_team",team_color="red",figure_n=1)
for tier_name in data_class.team["domestic_team"]["tier"].tier:
    test.bar_graph_n(
        data_class.team["domestic_team"]["tier"].tier[tier_name],
        bar_count=2,
        bar_num=1,
        team_color="blue",
        figure_n=tier_name,
    )
    test.bar_graph_n(
        data_class.team["foreigner_team"]["tier"].tier[tier_name],
        bar_count=2,
        bar_num=2,
        team_color="red",
        figure_n=tier_name,
    )
test.save()
print("end")


# import pprint

# emoticon_class = EmoticonMMRClass(split_range=1000)
# pprint.pprint(ERDataCleansing(30386977, 30386977, emoticon_class))

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
