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
