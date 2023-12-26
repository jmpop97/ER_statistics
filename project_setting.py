import json
import os
import importlib
import ER_apis.ER_api

if os.path.exists('setting') == False:
    os.mkdir('setting')
i=0
while i==0:
    Api_key=input('키를 입력하시오:')
    Api_key_dic={'token':Api_key}
    with open('setting\secret.json', 'w') as file:
        json.dump(Api_key_dic,file)
    print(Api_key_dic)

# 테스트용 데이터 하나 받기    

    importlib.reload(ER_apis.ER_api) 
    ER_apis.ER_api.save_games(31460173,1)
# 데이터가 받아졌는지로 키가 맞는지 아닌지 확인
    if os.path.isfile('./datas/Ver10.0_Rank_31460173.json') == False:
        print('잘못된 키가 입력되었습니다.')
    else:
        i+=1
        os.remove('./datas/Ver10.0_Rank_31460173.json')
        print('입력되었습니다.')