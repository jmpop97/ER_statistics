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
        self.assertTrue(check.tier["골드"][75] == 2 / check.total["골드"])


class TestEmoticonMMRClass(unittest.TestCase):
    test_list = [EmoticonMMRClass(split_range=250), EmoticonMMRClass(split_range=1000)]
    for test_element in test_list:
        ERDataCleansing(test_element, DB_type="test")

    CHECK_EMOTION_USED_LIST = [
        {
            750: [{"emoticon_count": 3, "gained_mmr": 4}],
            1000: [{"emoticon_count": 5, "gained_mmr": 17}],
            2750: [
                {"emoticon_count": 2, "gained_mmr": -19},
                {"emoticon_count": 5, "gained_mmr": 19},
            ],
            3250: [
                {"emoticon_count": 3, "gained_mmr": -25},
                {"emoticon_count": 4, "gained_mmr": -4},
                {"emoticon_count": 4, "gained_mmr": -4},
                {"emoticon_count": 0, "gained_mmr": -24},
                {"emoticon_count": 7, "gained_mmr": 47},
                {"emoticon_count": 0, "gained_mmr": -22},
                {"emoticon_count": 4, "gained_mmr": 47},
                {"emoticon_count": 4, "gained_mmr": 14},
            ],
            3750: [{"emoticon_count": 0, "gained_mmr": -21}],
            4000: [
                {"emoticon_count": 8, "gained_mmr": 7},
                {"emoticon_count": 3, "gained_mmr": -11},
                {"emoticon_count": 0, "gained_mmr": -10},
            ],
            4250: [
                {"emoticon_count": 2, "gained_mmr": -35},
                {"emoticon_count": 4, "gained_mmr": 49},
                {"emoticon_count": 2, "gained_mmr": -11},
                {"emoticon_count": 21, "gained_mmr": 2},
            ],
            4500: [
                {"emoticon_count": 3, "gained_mmr": -39},
                {"emoticon_count": 8, "gained_mmr": 44},
                {"emoticon_count": 0, "gained_mmr": -39},
                {"emoticon_count": 7, "gained_mmr": 44},
                {"emoticon_count": 4, "gained_mmr": -14},
                {"emoticon_count": 4, "gained_mmr": -29},
                {"emoticon_count": 0, "gained_mmr": -29},
                {"emoticon_count": 6, "gained_mmr": -15},
            ],
            4750: [
                {"emoticon_count": 2, "gained_mmr": -41},
                {"emoticon_count": 11, "gained_mmr": -7},
                {"emoticon_count": 5, "gained_mmr": -1},
            ],
            5000: [
                {"emoticon_count": 9, "gained_mmr": 58},
                {"emoticon_count": 6, "gained_mmr": 58},
                {"emoticon_count": 19, "gained_mmr": -20},
                {"emoticon_count": 5, "gained_mmr": -7},
                {"emoticon_count": 9, "gained_mmr": -6},
                {"emoticon_count": 2, "gained_mmr": -45},
                {"emoticon_count": 20, "gained_mmr": -50},
                {"emoticon_count": 13, "gained_mmr": 18},
                {"emoticon_count": 11, "gained_mmr": -6},
            ],
            5250: [
                {"emoticon_count": 8, "gained_mmr": 57},
                {"emoticon_count": 3, "gained_mmr": -46},
                {"emoticon_count": 3, "gained_mmr": -42},
                {"emoticon_count": 2, "gained_mmr": -46},
            ],
            5500: [
                {"emoticon_count": 2, "gained_mmr": 71},
                {"emoticon_count": 12, "gained_mmr": 71},
                {"emoticon_count": 7, "gained_mmr": 71},
            ],
            5750: [{"emoticon_count": 3, "gained_mmr": -44}],
        },
        {
            0: [{"emoticon_count": 3, "gained_mmr": 4}],
            1000: [{"emoticon_count": 5, "gained_mmr": 17}],
            2000: [
                {"emoticon_count": 2, "gained_mmr": -19},
                {"emoticon_count": 5, "gained_mmr": 19},
            ],
            3000: [
                {"emoticon_count": 3, "gained_mmr": -25},
                {"emoticon_count": 4, "gained_mmr": -4},
                {"emoticon_count": 4, "gained_mmr": -4},
                {"emoticon_count": 0, "gained_mmr": -24},
                {"emoticon_count": 7, "gained_mmr": 47},
                {"emoticon_count": 0, "gained_mmr": -22},
                {"emoticon_count": 4, "gained_mmr": 47},
                {"emoticon_count": 4, "gained_mmr": 14},
                {"emoticon_count": 0, "gained_mmr": -21},
            ],
            4000: [
                {"emoticon_count": 2, "gained_mmr": -41},
                {"emoticon_count": 3, "gained_mmr": -39},
                {"emoticon_count": 8, "gained_mmr": 44},
                {"emoticon_count": 0, "gained_mmr": -39},
                {"emoticon_count": 2, "gained_mmr": -35},
                {"emoticon_count": 8, "gained_mmr": 7},
                {"emoticon_count": 4, "gained_mmr": 49},
                {"emoticon_count": 7, "gained_mmr": 44},
                {"emoticon_count": 2, "gained_mmr": -11},
                {"emoticon_count": 3, "gained_mmr": -11},
                {"emoticon_count": 4, "gained_mmr": -14},
                {"emoticon_count": 21, "gained_mmr": 2},
                {"emoticon_count": 11, "gained_mmr": -7},
                {"emoticon_count": 4, "gained_mmr": -29},
                {"emoticon_count": 0, "gained_mmr": -29},
                {"emoticon_count": 5, "gained_mmr": -1},
                {"emoticon_count": 0, "gained_mmr": -10},
                {"emoticon_count": 6, "gained_mmr": -15},
            ],
            5000: [
                {"emoticon_count": 9, "gained_mmr": 58},
                {"emoticon_count": 6, "gained_mmr": 58},
                {"emoticon_count": 8, "gained_mmr": 57},
                {"emoticon_count": 19, "gained_mmr": -20},
                {"emoticon_count": 5, "gained_mmr": -7},
                {"emoticon_count": 9, "gained_mmr": -6},
                {"emoticon_count": 2, "gained_mmr": -45},
                {"emoticon_count": 3, "gained_mmr": -46},
                {"emoticon_count": 3, "gained_mmr": -42},
                {"emoticon_count": 20, "gained_mmr": -50},
                {"emoticon_count": 2, "gained_mmr": -46},
                {"emoticon_count": 3, "gained_mmr": -44},
                {"emoticon_count": 2, "gained_mmr": 71},
                {"emoticon_count": 12, "gained_mmr": 71},
                {"emoticon_count": 13, "gained_mmr": 18},
                {"emoticon_count": 7, "gained_mmr": 71},
                {"emoticon_count": 11, "gained_mmr": -6},
            ],
        },
    ]

    def test_split(self):
        self.test_list[0].dic_mmr_emoticon = dict(
            sorted(self.test_list[0].dic_mmr_emoticon.items())
        )
        self.test_list[1].dic_mmr_emoticon = dict(
            sorted(self.test_list[1].dic_mmr_emoticon.items())
        )

        check = [self.test_list[0].dic_mmr_emoticon, self.test_list[1].dic_mmr_emoticon]

        self.assertEqual(check, self.CHECK_EMOTION_USED_LIST)

    """
    def test_split1000(self):
        check = self.test.dic_mmr_emoticon
        self.assertTrue([len(check[:])]==self.CHECK_VALUE/check.total[""])
    """


"""
class TestCharacterClass(unittest.TestCase):
    test = CharacterClass()

    ERDataCleansing(test, DB_type="test")

    def test_percentage(self):
        check = self.test.dic_characterNum_percentage_datas
        self.assertEqual(check["tanker"], 0.2926829268292683)
        self.assertEqual(check["dealer"], 0.7073170731707317)
        self.assertEqual(check["support"], 0.0)

    def test_mean(self):
        check = self.test.dic_characterNum_mean_datas
        self.assertEqual(
            check,
            {
                "tanker": 2.6666666666666665,
                "dealer": 1.5263157894736843,
                "support": 0.0,
            },
        )

    def test_data(self):
        check = self.test.dic_characterNum_datas_list
        self.assertEqual(check["tanker"][2], 9)
        self.assertEqual(check["tanker"][4], 2)
        self.assertEqual(check["dealer"][1], 1)
        self.assertEqual(check["support"][0], 0)
    def test_data(self):
        check = self.test.dic_characterNum_datas_list
        self.assertEqual(check["tanker"][2], 9)
        self.assertEqual(check["tanker"][4], 2)
        self.assertEqual(check["dealer"][1], 1)
        self.assertEqual(check["support"][0], 0)
"""


class TestCamera(unittest.TestCase):
    test = Camera_All(
        "addSurveillanceCamera",
        "addTelephotoCamera",
        "mmrGainInGame",
        "mmrBefore",
        "gameRank",
        "characterNum",
    )
    ERDataCleansing(test, DB_type="test")

    def test_camera_mmr(self):
        check_mmr = self.test.dic_cameraGroup_mmr
        self.assertTrue(check_mmr[1] == 4.8)

    def test_camera_tier(self):
        check_tier = self.test.dic_cameraGroup_tier
        self.assertTrue(check_tier["브론즈"] == 3.0)

    def test_camera_rank(self):
        check_rank = self.test.dic_cameraGroup_Rank
        self.assertTrue(check_rank[1] == 15.5)

    def test_camera_Lukemai(self):
        check_Lukemai = self.test.dic_cameraGroup_LukeMai
        self.assertTrue(check_Lukemai["마이"] == 1.0)
