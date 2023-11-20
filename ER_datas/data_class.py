from function.public_function import emty_list
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
    
    def last_calculate(self):
        print("last")

class ForeignTeam(DataClass):
    def __init__(self,*conditions):
        self.conditions=conditions
        domestic_team={}
        for condition in self.conditions:
            domestic_team[condition]=[]
        foreigner_team={}
        for condition in self.conditions:
            foreigner_team[condition]=[]


        self.team={"domestic_team":domestic_team,
                   "foreigner_team":foreigner_team}
        self.memory={}
        self._memory_reset()

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
            foreigner_team=self.team["foreigner_team"]
            for condition in self.conditions:
                foreigner_team[condition]+=[user_data[condition]]            
            return
        else:
            pass
        memory["state"]+=1
        '''다함'''
        if memory["state"]==3:
            domestic_team=self.team["domestic_team"]
            for condition in self.conditions:
                domestic_team[condition]+=[user_data[condition]]   
            

    def _memory_reset(self):    
        for i in range(1,9):
            memory_i={}
            memory_i["state"]=0
            memory_i["language"]=""
            memory_i["mmrGainInGame"]=0
            memory_i["gameRank"]=0
            self.memory[i]=memory_i
        
    def add_data_game_id(self, user_data):
        self._memory_reset()