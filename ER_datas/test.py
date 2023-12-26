import json

with open("./datas/Ver9.0_Rank_31131392.json", "r", encoding="utf-8") as f:
    test_data1 = json.load(f)
with open("./datas/Ver9.0_Rank_31130633.json", "r", encoding="utf-8") as f:
    test_datas = json.load(f)

from .ERDataCleansing import ERDataCleansing
from .data_class import *
import unittest


class TestERDataCleansing(unittest.TestCase):
    test = TestClass()
    ERDataCleansing(data_class=test, DB_type="test")

    def test_add_data(self):
        self.assertTrue(self.test.count_add_data == 48)

    def test_add_data_game_id(self):
        self.assertTrue(self.test.count_add_data_game_id == 2)

    def test_last(self):
        self.assertTrue(self.test.count_last_calculate == 1)

    def test_add_user_data(self):
        self.assertTrue(self.test.user_data["userNum"] == 71183)


class TestDicCharacterFilterData(unittest.TestCase):
    test = DicCharacterFilterData("mmrBefore", "gameRank")
    ERDataCleansing(data_class=test, DB_type="test")

    def test_add_user_data(self):
        self.assertTrue(
            self.test.dic_characterNum_datas[42][1]
            == {"mmrBefore": 5085, "gameRank": 3}
        )


class TestListFilterData(unittest.TestCase):
    dic_name = {"10*gameRank": "gameRank10"}
    test = ListFilterData(
        "playTime", "mmrGainInGame", "gameRank", "10*gameRank", **dic_name
    )
    ERDataCleansing(test, DB_type="test")

    def test_add_user_data(self):
        self.assertTrue(self.test.conditions["playTime"][-2] == 929)

    def test_name_error(self):
        self.assertTrue(self.test.conditions.get("gameRank10", [3])[0] == 80)

    def test_caculate_error(self):
        self.assertTrue(self.test.conditions["gameRank10"][1] == 70)


class TestForeignTeam(unittest.TestCase):
    test = ForeignTeam("gameRank", "mmrBefore")
    ERDataCleansing(test, DB_type="test")

    def test_condition(self):
        check = self.test.team["foreigner_team"]["mmrBefore"]
        self.assertTrue(check[1] == 4572)
        self.assertTrue(check[4] == 5000)

    def test_tier(self):
        check = self.test.team["domestic_team"]["tier"]
        print(check.tier["골드"])
        print(check.total["골드"])
        self.assertTrue(check.tier["골드"][75] == 2 / check.total["골드"])
