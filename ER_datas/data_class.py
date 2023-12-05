from typing import Any
from function.public_function import emty_list
from .tier_mmr import Tier
import numpy as np
from read_txt import LoadCharacter
import json


class DataClass:
    def add_data(self, user_data):
        print("not add_data")

    def add_data_game_id(self):
        print("not add_data_game_id")

    def last_calculate(self):
        print("not last_calculate")


class FilterData(DataClass):
    def __init__(self, *condition):
        self.dic_characterNum_datas = {}
        self.condition = condition

    def add_data(self, user_data):
        characterNum = user_data["characterNum"]
        datas = {}
        list_request_datatype = self.condition
        for request_datatype in list_request_datatype:
            datas[request_datatype] = user_data[request_datatype]
            self.dic_characterNum_datas[characterNum] = self.dic_characterNum_datas.get(
                characterNum, []
            ) + [datas]


class ForeignTeam(DataClass):
    def __init__(self, *conditions):
        self.conditions = conditions
        self.team = {
            "domestic_team": self._team_db_setting(),
            "foreigner_team": self._team_db_setting(),
        }
        self.memory = {}
        self._memory_reset()

    def _team_db_setting(self):
        db = {}
        db["tier"] = Tier()
        for condition in self.conditions:
            db[condition] = []
        return db

    def _memory_reset(self):
        for i in range(1, 9):
            memory_i = {}
            memory_i["state"] = 0
            memory_i["language"] = ""
            for condition in self.conditions:
                memory_i[condition] = []
            self.memory[i] = memory_i

    def add_data(self, user_data):
        # 입력 내용
        teamNumber = user_data["teamNumber"]
        memory = self.memory[teamNumber]

        """미확인"""
        _language = user_data.get("language", "error")
        if memory["state"] == 0:
            memory["language"] = _language
        elif memory["language"] != _language:
            memory["state"] = -1

        for condition in self.conditions:
            memory[condition] += [user_data[condition]]
        if memory["state"] != -1:
            memory["state"] += 1

    def add_data_game_id(self):
        for team_id in self.memory:
            if self.memory[team_id]["state"] == 3:
                self._add_team_data("domestic_team", self.memory[team_id])
            elif self.memory[team_id]["state"] == -1:
                self._add_team_data("foreigner_team", self.memory[team_id])
            else:
                pass

        self._memory_reset()

    def _add_team_data(self, key, memory):
        team = self.team[key]
        for team_mate in range(0, 3):
            team["tier"].split_tier(
                memory["mmrBefore"][team_mate], memory["mmrGainInGame"][team_mate]
            )
        for condition in self.conditions:
            team[condition] += [memory[condition]]

    def last_calculate(self):
        print("last_calcu")
        teams = self.team
        for team in teams:
            print("team", team)
            teams[team]["tier"].mean()


# 이모티콘 소통의 유의미 한가?(현 mmr, 획득 mmr)
class EmoticonMMRClass(DataClass):
    def __init__(self, split_range, *condition):
        self.dic_mmr_emoticon = {}
        self.split_range = split_range
        self.condition = condition

    def add_data(self, user_data):
        datas = {}
        user_mmr = int(user_data["mmrBefore"] / self.split_range) * self.split_range
        if self.dic_mmr_emoticon.get(user_mmr) == None:
            datas[user_mmr] = []
        else:
            datas[user_mmr] = self.dic_mmr_emoticon[user_mmr]
        self.dic_mmr_emoticon[user_mmr] = datas[user_mmr] + [
            {
                "emoticon_count": user_data["useEmoticonCount"],
                "gained_mmr": user_data["mmrGain"],
            }
        ]

    def last_calculate(self):
        data = {"sum": {}, "mean": {}}
        for mmr in self.dic_mmr_emoticon:
            emoticon_count = int(
                sum(data["emoticon_count"] for data in self.dic_mmr_emoticon[mmr])
            )
            gained_mmr = sum(data["gained_mmr"] for data in self.dic_mmr_emoticon[mmr])
            data["sum"][mmr] = {
                "emoticon_count": emoticon_count,
                "gained_mmr": gained_mmr,
            }
            data["mean"][mmr] = {
                "emoticon_count": emoticon_count / len(self.dic_mmr_emoticon[mmr]),
                "gained_mmr": gained_mmr / len(self.dic_mmr_emoticon[mmr]),
            }
        return data

    def get_data(self):
        return self.dic_mmr_emoticon


# 보안 콘솔을 자주 키는 험체(탱커, 딜러)
class CharacterClass(DataClass):
    def __init__(self, *condition):
        self.dic_characterNum_datas = {"tanker": 0, "dealer": 0, "support": 0}
        self.dic_character_class = {}
        self.dic_characterNum_datas_list = {"tanker": [], "dealer": [], "support": []}
        with open("class.json", "r", encoding="utf-8") as class_json_file:
            self.dic_character_class = json.load(class_json_file)
        self.condition = condition

    def add_data(self, user_data):
        character_name = LoadCharacter()
        characterNum = user_data["characterNum"]
        str_user_character_name = character_name[str(characterNum)]
        str_user_character_class = "dealer"
        if str_user_character_name in self.dic_character_class["tanker"]:
            str_user_character_class = "tanker"
        elif str_user_character_name in self.dic_character_class["support"]:
            str_user_character_class = "support"
        used_security_console = user_data["useSecurityConsole"]
        datas = used_security_console

        self.dic_characterNum_datas_list[str_user_character_class].append(datas)

    def last_calculate(self):
        datas = {}
        for class_key in self.dic_characterNum_datas_list:
            datas[class_key] = np.mean(self.dic_characterNum_datas_list[class_key])
        return datas

    def get_data(self):
        return self.dic_characterNum_datas_list


# #카메라 통합
class Camera_All(DataClass):
    def __init__(self, *condition):
        self.condition = condition
        self.dic_cameraGroup_mmr = {}
        self.dic_cameraGroup_tier = {}
        self.dic_cameraGroup_Rank = {}
        self.dic_cameraGroup_LukeMai = {"나머지": []}
        self.tier_range = {}
        self.tier_range[0] = "아이언"
        self.tier_range[1000] = "브론즈"
        self.tier_range[2000] = "실버"
        self.tier_range[3000] = "골드"
        self.tier_range[4000] = "플레티넘"
        self.tier_range[5000] = "다이아"
        self.tier_range[6000] = "데미갓"
        self.tier_range["all"] = "all"

    def add_data(self, user_data):
        # #총 카메라 수
        addScamera = user_data["addSurveillanceCamera"]
        addTcamera = user_data["addTelephotoCamera"]
        addCamera = addTcamera + addScamera
        # #카메라 설치 수에 따른 mmr 증가량
        mmrGainIngame = user_data["mmrGainInGame"]
        self.dic_cameraGroup_mmr[addCamera] = self.dic_cameraGroup_mmr.get(
            addCamera, []
        ) + [mmrGainIngame]

        # #티어 별 카메라 설치 평균
        mmrBefore = user_data["mmrBefore"]
        if mmrBefore > 6000:
            mmrBefore = 6000
        mmrBefore_thousand = (mmrBefore % 10000 // 1000) * 1000
        tier = self.tier_range[mmrBefore_thousand]
        self.dic_cameraGroup_tier[tier] = self.dic_cameraGroup_tier.get(tier, []) + [
            addCamera
        ]

        # #등수 별 카메라 설치 평균
        gameRank = user_data["gameRank"]
        self.dic_cameraGroup_Rank[gameRank] = self.dic_cameraGroup_Rank.get(
            gameRank, []
        ) + [addCamera]

        # #루크/마이의 카메라 설치 평균
        character_name = LoadCharacter()
        characterNum = user_data["characterNum"]
        str_characterNum = str(characterNum)
        if characterNum == 22:
            self.dic_cameraGroup_LukeMai[
                character_name[str_characterNum]
            ] = self.dic_cameraGroup_LukeMai.get(
                character_name[str_characterNum], []
            ) + [
                addCamera
            ]
        elif characterNum == 45:
            self.dic_cameraGroup_LukeMai[
                character_name[str_characterNum]
            ] = self.dic_cameraGroup_LukeMai.get(
                character_name[str_characterNum], []
            ) + [
                addCamera
            ]
        else:
            self.dic_cameraGroup_LukeMai["나머지"].append(addCamera)

    def last_calculate(self):
        # #카메라 설치 수에 따른 mmr 증가량
        for key in self.dic_cameraGroup_mmr:
            self.dic_cameraGroup_mmr[key] = np.mean(self.dic_cameraGroup_mmr[key])
        self.dic_cameraGroup_mmr = dict(
            sorted(self.dic_cameraGroup_mmr.items(), key=lambda x: x[0])
        )

        # #티어 별 카메라 설치 평균
        for tier in self.dic_cameraGroup_tier:
            self.dic_cameraGroup_tier[tier] = np.mean(self.dic_cameraGroup_tier[tier])
        rank_order = ["아이언", "브론즈", "실버", "골드", "플레티넘", "다이아", "데미갓"]
        self.dic_cameraGroup_tier = {
            key: value
            for key, value in sorted(
                self.dic_cameraGroup_tier.items(), key=lambda x: rank_order.index(x[0])
            )
        }

        # #등수 별 카메라 설치 평균
        for gameRank in self.dic_cameraGroup_Rank:
            self.dic_cameraGroup_Rank[gameRank] = np.mean(
                self.dic_cameraGroup_Rank[gameRank]
            )
        self.dic_cameraGroup_Rank = dict(
            sorted(self.dic_cameraGroup_Rank.items(), key=lambda x: x[0])
        )

        # #루크/마이의 카메라 설치 평균 수
        for character in self.dic_cameraGroup_LukeMai:
            self.dic_cameraGroup_LukeMai[character] = np.mean(
                self.dic_cameraGroup_LukeMai[character]
            )


# #크레딧으로 빌드업 템 만드는것과 후반 보면서 빌드하는 것에 차이(gainMMR)
# class CreditBuildUpMMR(DataClass):
#     def __init__(self) -> None:
#         super().__init__()

#     def add_data(self, user_data):
#         return super().add_data(user_data)

#     def last_calculate(self):
#         return super().last_calculate()
