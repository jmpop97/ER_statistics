from function.public_function import emty_list
from .tier_mmr import Tier

class DataClass:
    def add_data(self,user_data):
        print("not add_data")
    def add_data_game_id(self,user_data):
        print("not add_data_game_id")
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

class ForeignTeam(DataClass):
    def __init__(self,*conditions):
        self.conditions=conditions
        self.team={"domestic_team":self._team_db_setting(),
                   "foreigner_team":self._team_db_setting()}
        self.memory={}
        self._memory_reset()

    def _team_db_setting(self):
        db={}
        db["tier"]=Tier()
        for condition in self.conditions:
            db[condition]=[]
        return db
    
    def _memory_reset(self):    
        for i in range(1,9):
            memory_i={}
            memory_i["state"]=0
            memory_i["language"]=""
            memory_i["mmrGainInGame"]=0
            memory_i["gameRank"]=0
            self.memory[i]=memory_i
    

    def add_data(self, user_data):
        #입력 내용
        teamNumber=user_data["teamNumber"]
        memory=self.memory[teamNumber]
        '''외국팀'''
        if memory["state"]==-1:
            return
        '''미확인'''
        if memory["state"]==0:
            memory["language"]=user_data["language"]
            for condition in self.conditions:
                memory[condition]=user_data[condition]
        elif memory["language"]!=user_data["language"]:
            memory["state"]=-1
            self._add_team_data("foreigner_team",user_data)  
            return
        else:
            pass
        memory["state"]+=1
        '''국내팀'''
        if memory["state"]==3:
            self._add_team_data("domestic_team",user_data)            
    def _add_team_data(self,key,user_data):
        team=self.team[key]
        team["tier"].split_tier(user_data["mmrBefore"],user_data["mmrGainInGame"])
        for condition in self.conditions:
            team[condition]+=[user_data[condition]]            
        

    def add_data_game_id(self, user_data):
        self._memory_reset()

    def last_calculate(self):
        teams=self.team
        for team in teams:
            teams[team]["tier"].mean()