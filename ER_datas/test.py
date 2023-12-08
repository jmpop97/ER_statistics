import json

with open("./datas/Ver9.0_Rank_31131392.json", "r", encoding="utf-8") as f:
    test_data1 = json.load(f)
with open("./datas/Ver9.0_Rank_31130633.json", "r", encoding="utf-8") as f:
    test_datas = json.load(f)


from .ERDataCleansing import ERDataCleansing
from .data_class import *

test = TestClass()
ERDataCleansing(data_class=test, test=True)
if test.count_add_data != 48:
    raise Exception("add_data")
if test.count_add_data_game_id != 2:
    raise Exception("add_data_game_id")
if test.count_last_calculate != 1:
    raise Exception("last_calculate")
if test.user_data["userNum"] != 71183:
    raise Exception("add_user_data")
