#save api datas
# from ER_apis.ER_api import save_games
# save_games(30306839,30306839+1000)


#sort datas
from ER_datas.ERDataCleansing import ERDataCleansing
from ER_datas.data_class import *
data_class=ForeignTeam("mmrBefore","mmrGainInGame","gameRank")
ERDataCleansing(30306839,30306839+1000,data_class)
print(data_class.team["domestic_team"]["tier"].tier["all"])

#figure
from ER_fig.figure_datas import FigureType
test=FigureType()
# test.scatterplot(data_class.team["domestic_team"],"mmrGainInGame","mmrBefore",titles="domestic_team",team_color="blue",figure_n=1)
# test.scatterplot(data_class.team["foreigner_team"],"mmrGainInGame","mmrBefore",titles="foreign_team",team_color="red",figure_n=1)
for tier_name in data_class.team["domestic_team"]["tier"].tier:
    test.bar_graph(data_class.team["domestic_team"]["tier"].tier[tier_name],bar_count=2,bar_num=1,team_color="blue",figure_n=tier_name)
    test.bar_graph(data_class.team["foreigner_team"]["tier"].tier[tier_name],bar_count=2,bar_num=2,team_color="red",figure_n=tier_name)

test.show()
