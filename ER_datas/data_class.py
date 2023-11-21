class DataClass:
    def add_data(self,user_data):
        print("not add_data")
    def last_calculate(self):
        print("not last_calculate")


class FilterData(DataClass):
    def __init__(self,*condition):
        self.dic_characterNum_datas={}
        self.condition=condition

    def add_data(self,user_data):
        characterNum=user_data["characterNum"]
        datas={}
        list_request_datatype=self.condition
        for request_datatype in list_request_datatype:
            datas[request_datatype]=user_data[request_datatype]
            self.dic_characterNum_datas[characterNum]=self.dic_characterNum_datas.get(characterNum,[])+[datas]
    
    def last_calculate(self):
        print("last")

import numpy as np
from read_txt import LoadCharacter
import json

# 이모티콘 소통의 유의미 한가?(현 mmr, 획득 mmr)
class EmoticonMMRClass(DataClass):
    def __init__(self, split_range, *condition):
        self.dic_mmr_emoticon={}
        self.split_range = split_range
        self.condition=condition
    
    def add_data(self, user_data):
        datas={}
        user_mmr = int(user_data["mmrBefore"]/self.split_range)*self.split_range
        if self.dic_mmr_emoticon.get(user_mmr)==None:
            datas[user_mmr]=[]
        else:
             datas[user_mmr]=self.dic_mmr_emoticon[user_mmr]
        self.dic_mmr_emoticon[user_mmr] = datas[user_mmr]+[{"emoticon_count":user_data["useEmoticonCount"], "gained_mmr":user_data["mmrGain"]}]
    
    def last_calculate(self):
        data={"sum":{}, "mean":{}}
        for mmr in self.dic_mmr_emoticon:
            emoticon_count = int(sum(data["emoticon_count"] for data in self.dic_mmr_emoticon[mmr]))
            gained_mmr = sum(data["gained_mmr"] for data in self.dic_mmr_emoticon[mmr])
            data["sum"][mmr]={"emoticon_count":emoticon_count, "gained_mmr":gained_mmr}
            data["mean"][mmr]={"emoticon_count":emoticon_count/len(self.dic_mmr_emoticon[mmr]),
                                "gained_mmr":gained_mmr/len(self.dic_mmr_emoticon[mmr])}
        return data
    def get_data(self):
        return self.dic_mmr_emoticon
    
# 보안 콘솔을 자주 키는 험체(탱커, 딜러)
class CharacterClass(DataClass):
    def __init__(self, *condition):
        self.dic_characterNum_datas={"tanker":0,
                         "dealer":0,
                         "support":0}
        self.dic_character_class={}
        self.dic_characterNum_datas_list={"tanker":[],
                         "dealer":[],
                         "support":[]}
        with open("class.json", "r", encoding='utf-8') as class_json_file:
            self.dic_character_class=json.load(class_json_file)
        self.condition = condition 
    def add_data(self, user_data):
        character_name = LoadCharacter()
        characterNum=user_data["characterNum"]
        str_user_character_name = character_name[str(characterNum)]
        str_user_character_class='dealer'
        if (str_user_character_name in self.dic_character_class['tanker']):
            str_user_character_class = 'tanker'
        elif (str_user_character_name in self.dic_character_class['support']):
            str_user_character_class = 'support'
        used_security_console = user_data["useSecurityConsole"]
        datas=used_security_console
        
        self.dic_characterNum_datas_list[str_user_character_class].append(datas)

    def last_calculate(self):
        datas={}
        for class_key in self.dic_characterNum_datas_list:
            datas[class_key]=np.mean(self.dic_characterNum_datas_list[class_key])
        return datas
    
    def get_data(self):
        return self.dic_characterNum_datas_list

# 크레딧으로 빌드업 템 만드는것과 후반 보면서 빌드하는 것에 차이(gainMMR)
class CreditBuildUpMMR(DataClass):
    def __init__(self) -> None:
        super().__init__()
    def add_data(self, user_data):
        return super().add_data(user_data)
    def last_calculate(self):
        return super().last_calculate()


class ForeignTeam(DataClass):
    def __init__(self):
        self.team={{"foreign_team":{}, 
                   "domestic_team":{}}}
        self.team_room={}
    def add_data(self, user_data):
        self.team_room=self.team_room.get("teamNumber", [])+[]

    def add_data_game_id(self, user_data):
        return