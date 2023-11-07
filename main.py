#save api datas
#from ER_apis.ER_api import save_games
#save_games(27721413,27721414)



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
import os
os.system("cls")
from ER_datas.ERDataCleansing import ERDataCleansing
data_type="test"
list_request_datatype=["maxHp","gameRank"]
dic_characterNum_datas=ERDataCleansing(29889463,29889463,data_type,list_request_datatype)
#figure 
# from ER_fig.figure_datas import figure_save
# figure_type="plot_mmrcharge"
# list_request_datatype=["mmrBefore","mmrGain"]
# figure_save(dic_characterNum_datas,figure_type,list_request_datatype)


