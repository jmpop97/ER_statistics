# save api datas
# sort datas
from ER_apis.ER_api import save_games

# save_games(30610390,100)


from ER_datas.ERDataCleansing import ERDataCleansing
from ER_datas.data_class import *

"""example FilterData class"""
# data_class=FilterData("mmrBefore","mmrGain")
# ERDataCleansing(27619195,27621220,data_class)
# character_console_class=CharacterClass("")
# print(ERDataCleansing(30383343,30386977,character_console_class))
# print(character_console_class.get_data())

"""example ForeignTeam class"""
# sort datas
data_class = ForeignTeam("mmrBefore", "mmrGainInGame", "gameRank")
ERDataCleansing(30306839, 30306839 + 1000, data_class)
print(data_class.team["domestic_team"]["tier"].total)

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
test.show()


# import pprint

# emoticon_class = EmoticonMMRClass(split_range=1000)
# pprint.pprint(ERDataCleansing(30386977, 30386977, emoticon_class))

"""
#figure 
# from ER_fig.figure_datas import figure_save
# figure_type="range_split_mmr"
# list_request_datatype=["mmrBefore","mmrGain"]
# # figure_save(dic_characterNum_datas,figure_type,list_request_datatype)
"""
