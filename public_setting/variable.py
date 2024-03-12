import json
import os
from glob import glob
import itertools


class Tier:
    def __init__(self) -> None:
        with open("./handmadeDB/TierMMRCost/V15/Tier.json", "r", encoding="utf-8") as f:
            self.tier_DB = json.load(f)
        self.tier_DB.pop("name")
        self.tier_names = [name for [name, _, _, _] in self.tier_DB.values()]

    def tier_name(self, mmr: int = 0) -> str:
        for name, start, end, cost in self.tier_DB.values():
            if start <= mmr < end:
                return name
        return name

    def tier_cost(self, n) -> int:
        """n can tier name or mmrBefore"""
        if isinstance(n, str):
            for name, start, end, cost in self.tier_DB.values():
                if n == name:
                    return cost
            return cost
        else:
            for name, start, end, cost in self.tier_DB.values():
                if start <= n < end:
                    return cost
            cost += ((n - start) // end) * 2
            return cost
            print("int")
        # for tier_name,start,end,cost in self.tier_DB.values():
        #     if tier_name==name:
        #         return cost
        # return name


class game_DB:
    def __init__(self, types: list = ["Colbalt", "Normal", "Rank"]) -> None:
        self.root_dir = os.environ.get("GAME_DB", "./datas")
        self.DB_list = []
        self.types = ["Colbalt", "Normal", "Rank"]

    def set_DB_list(
        self,
        types: list = ["Colbalt", "Normal", "Rank"],
        major_version: int = [13],
        minor_version: int = [0],
    ):
        if types != ["Colbalt", "Normal", "Rank"]:
            self.types = types

        cases = list(itertools.product(major_version, minor_version, self.types))
        for major_ver, minor_ver, type_name in cases:
            self.DB_list += glob(
                f"{self.root_dir}/Ver{major_ver}.{minor_ver}_{type_name}*"
            )
        return self.DB_list
