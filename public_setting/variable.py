import json


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


a = Tier().tier_cost(6400)
print(a)
