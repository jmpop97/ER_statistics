# Before exec Update Game Base Data
from ER_datas.update_game_base_data import update_game_base_data

update_game_base_data()

# save api datas
from ER_apis.ER_api import save_games

save_games(start_game=31077018, n=1, second=1, game_type=["Normal"])
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
from ER_apis.ER_DB import create_query_gameId, create_query_version

data_class = ForeignTeam("mmrBefore", "mmrGainInGame", "gameRank")
ERDataCleansing(
    data_class, dbQuery=create_query_gameId(fromGameId=30769613, toGameId=30772611)
)
print("domestic_team", data_class.team["domestic_team"]["tier"].total)
print("foreigner_team", data_class.team["foreigner_team"]["tier"].total)

# figure
from ER_fig.figure_datas import FigureType

test = FigureType()
# test.scatterplot(data_class.team["domestic_team"],"mmrGainInGame","mmrBefore",titles="domestic_team",team_color="blue",figure_n=1)
# test.scatterplot(data_class.team["foreigner_team"],"mmrGainInGame","mmrBefore",titles="foreign_team",team_color="red",figure_n=1)
for tier_name in data_class.team["domestic_team"]["tier"].tier:
    test.bar_graph(
        data_class.team["domestic_team"]["tier"].tier[tier_name],
        bar_count=2,
        bar_num=1,
        team_color="blue",
        figure_n=tier_name,
    )
    test.bar_graph(
        data_class.team["foreigner_team"]["tier"].tier[tier_name],
        bar_count=2,
        bar_num=2,
        team_color="red",
        figure_n=tier_name,
    )
# test.show()


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
