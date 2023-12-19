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


test = DicCharacterFilterData("mmrBefore", "gameRank")
ERDataCleansing(data_class=test, test=True)
if test.dic_characterNum_datas[42][1] != {"mmrBefore": 5085, "gameRank": 3}:
    raise Exception("add_user_data")

dic_name = {"10*gameRank": "gameRank10"}
test = ListFilterData(
    "playTime", "mmrGainInGame", "gameRank", "10*gameRank", **dic_name
)
ERDataCleansing(test, test=True)
if test.conditions["playTime"] != [
    245,
    301,
    245,
    1086,
    245,
    301,
    301,
    1233,
    587,
    1087,
    1087,
    321,
    334,
    321,
    334,
    1233,
    587,
    1233,
    1233,
    1233,
    587,
    1233,
    321,
    334,
    771,
    231,
    231,
    230,
    711,
    231,
    348,
    230,
    1059,
    230,
    1248,
    1059,
    1245,
    348,
    1248,
    348,
    1059,
    1248,
    1248,
    1243,
    929,
    929,
    929,
    716,
]:
    raise Exception("add_user_data")
if not test.conditions.get("gameRank10", False):
    raise Exception("name_error")
if test.conditions["gameRank10"] != [
    80,
    70,
    80,
    30,
    80,
    70,
    70,
    10,
    40,
    30,
    30,
    60,
    50,
    60,
    50,
    10,
    40,
    20,
    20,
    10,
    40,
    20,
    60,
    50,
    50,
    70,
    70,
    80,
    50,
    70,
    60,
    80,
    30,
    80,
    10,
    30,
    20,
    60,
    10,
    60,
    30,
    10,
    20,
    20,
    40,
    40,
    40,
    50,
]:
    raise Exception("caculate_error")
