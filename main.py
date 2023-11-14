#save api datas
from ER_apis.ER_api import save_games
save_games(29889463,29889463)



#doc string
dic_dataType_figureType={
    "data_type":{"figure_type":{"data_condition":[]}}
    ,

    "filter": {"!*":{"condition:datas"}},
    "data_cleansing":{
        "plot":{"condition":["*","*"]},
        "plot_mmrcharge":{"condition":["mmrBefore","mmrGain"]}},
    "mmrGain_option": {
        "plot":{"condition":["*"]},
        "plot_mmrcharge":{"condition":["mmrBefore"]}
    }
           }
#sort datas
from ER_datas.ERDataCleansing import ERDataCleansing
from ER_datas.data_class import *
data_class=FilterData("mmrBefore","mmrGain")
ERDataCleansing(27619195,27621220,data_class)


#figure 
# from ER_fig.figure_datas import figure_save
# figure_type="range_split_mmr"
# list_request_datatype=["mmrBefore","mmrGain"]
# # figure_save(dic_characterNum_datas,figure_type,list_request_datatype)


