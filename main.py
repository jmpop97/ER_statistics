#save api datas
from ER_apis.ER_api import save_games
#save_games(27721413,27721414)



#doc string
dic_dataType_figureType={
    "filter": {
        "character_id":{"condition:datas"}},
    "data_cleansing":{
        "plot":{"condition":["*","*"]},
        "plot_mmrcharge":{"condition":["mmrBefore","mmrGain"]}}
           }
#sort datas
from ER_datas.ERDataCleansing import ERDataCleansing
data_type="data_cleansing"
list_request_datatype=["mmrBefore","mmrGain"]
dic_characterNum_datas=ERDataCleansing(27619195,27621220,data_type,list_request_datatype)
#figure 
from ER_fig.figure_datas import figure_save
figure_type="plot_mmrcharge"
figure_save(dic_characterNum_datas,figure_type,list_request_datatype)


    

