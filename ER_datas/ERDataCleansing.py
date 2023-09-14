import os
os.system('cls')

# 캐릭터 이름
'''
dic_characterNum_characterName[characterNum] = 캐릭터명
dic_characterNum_characterCount[characterNum] = 캐릭터별 빈도
dic_characterNum_BeforeMMR[characterNum]= {BeforeMMR:dic_BeforeMMR_datas}
dic_BeforeMMR_datas
=[{         
    "mmrGain": 얻은점수,
    "gameRank":게임 순위,
    "escapeState":탈출유무
 }]
'''

#game_data 가져오기

import json

def ERDataCleansing(start_point,end_point,type,condition):
    datas_num=start_point
    result_data=FilterType(type,condition)
    while datas_num<=end_point:
        # 데이터 읽기
        with open(f"datas/{datas_num}.json", "r", encoding='utf-8') as f:
            game_datas = json.load(f)
        datas_num+=1
        
        # 404 error
        if game_datas["code"]==404:
            continue
        
        # 일반제거
        game_type=game_datas["userGames"][0]["matchingMode"]
        if game_type==2 or game_type==6:
            continue

        for user_data in game_datas["userGames"]:
            '''유저 정보'''
            result_data.result(user_data)

             # data_cleansing[mmrBefore]=data_cleansing.get(mmrBefore,[])+[mmrGain]
        

    return result_data

class FilterType():
    '''type=filter
    dic_characterNum_datas[condition]=datas
    '''
    def filter_data_init(self):
        self.dic_characterNum_datas={}

    
    def filter_data(self,user_data):
        characterNum=user_data["characterNum"]
        datas={}
        list_request_datatype=self.condition
        for request_datatype in list_request_datatype:
            datas[request_datatype]=user_data[request_datatype]
            self.dic_characterNum_datas[characterNum]=self.dic_characterNum_datas.get(characterNum,[])+[datas]

    
    '''type=data_cleansing

    '''
    def data_cleansing_init(self):
        self.dic_characterNum_datas={}

    
    def data_cleansing(self,user_data):

        characterNum=user_data["characterNum"]
        dic_characterNum_datas=self.dic_characterNum_datas.get(characterNum,{})
        for condition in self.condition:
            data=user_data[condition]
            dic_characterNum_datas[condition]=dic_characterNum_datas.get(condition,[])+[data]
        self.dic_characterNum_datas[characterNum]=dic_characterNum_datas

    dic_type_init={
        "filter": filter_data_init,
        "data_cleansing": data_cleansing_init
    }
    dic_type_result={
        "filter": filter_data,
        "data_cleansing": data_cleansing
    }
    
    '''setting'''
    def __init__(self,type,condition):
        self.type=type
        self.condition=condition
        self.dic_type_init[type](self)
        pass
    '''add result'''
    def result(self,user_data):
        self.dic_type_result[self.type](self,user_data)

# list_request_datatype=["mmrBefore","mmrGain"]
# dic_characterNum_datas=ERDataCleansing(27619195,27621220,"data_cleansing",["mmrBefore","mmrGain"])
# print(dic_characterNum_datas.dic_characterNum_datas)

    