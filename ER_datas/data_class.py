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

class EmoticonMMRClass(DataClass):
    def __init__(self, split_range):
        self.dic_datas={}
        self.split_range = split_range
    
    def add_data(self, user_data):
        datas={}
        user_mmr = int(user_data["mmrBefore"]/self.split_range)
        if self.dic_datas.get(user_mmr)==None:
            datas[user_mmr]=[]
        else:
             datas[user_mmr]=self.dic_datas[user_mmr]
        self.dic_datas[user_mmr] = datas[user_mmr]+[user_data["useEmoticonCount"]]


    def last_calculate(self):
        data={"sum":{}, "mean":{}}
        for mmr in self.dic_datas:
            data["sum"][mmr]=np.sum(self.dic_datas[mmr])
            data["mean"][mmr]=np.mean(self.dic_datas[mmr])
        return data
    def get_data(self):
        return self.dic_datas
from read_txt import LoadCharacter

class CharacterClass(DataClass):
    def __init__(self, *condition):
        self.dic_characterNum_datas={"tanker":0,
                         "dealer":0,
                         "support":0}
        
        self.dic_characterNum_datas_list={"tanker":[],
                         "dealer":[],
                         "support":[]}
        
        self.dic_character_class={'tanker':[], 'support':[], 'dealer':[]}
        self.dic_character_class['tanker']=["매그너스", "현우", "쇼우", "키아라", "레온", "일레븐", "클로에", "에키온","마이", "엘레나", "마커스", "알론소"]
        self.dic_character_class['support']=["요한", "프리야", "아르다", "레니"]
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

        self.dic_characterNum_datas[str_user_character_class]=self.dic_characterNum_datas.get(str_user_character_class)+datas
        self.dic_characterNum_datas_list[str_user_character_class].append(datas)
        
    def last_calculate(self):
        datas=self.dic_characterNum_datas
        return datas
        
class ForeignTeam(DataClass):
    def __init__(self):
        self.team={{"foreign_team":{}, 
                   "domestic_team":{}}}
        self.team_room={}
    def add_data(self, user_data):
        self.team_room=self.team_room.get("teamNumber", [])+[]

    def add_data_game_id(self, user_data):
        return