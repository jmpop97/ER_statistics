tier_range = {}
tier_range[0] = "아이언"
tier_range[1000] = "브론즈"
tier_range[2000] = "실버"
tier_range[3000] = "골드"
tier_range[4000] = "플레티넘"
tier_range[5000] = "다이아"
tier_range[6000] = "데미갓"
tier_range["all"] = "all"

mmrGain_range = {}
mmrGain_range[0] = "0~24"
mmrGain_range[25] = "25~49"
mmrGain_range[50] = "50~74"
mmrGain_range[75] = "75~99"
mmrGain_range[100] = "100~124"
mmrGain_range[125] = "125~149"
mmrGain_range[150] = "150~174"
mmrGain_range[175] = "175~199"
mmrGain_range[200] = "200~224"
mmrGain_range[225] = "225~"


class Tier:
    def __init__(self):
        self.tier = {}
        self.tier["아이언"] = {}
        self.tier["브론즈"] = {}
        self.tier["실버"] = {}
        self.tier["골드"] = {}
        self.tier["플레티넘"] = {}
        self.tier["다이아"] = {}
        self.tier["데미갓"] = {}
        self.tier["all"] = {}
        self.total = {}

    def _split_mmrGain(self, mmrGain):
        mmrGain_range = [0, 25, 50, 75, 100, 125, 150, 175, 200, 225]
        while mmrGain_range:
            mmrGain_min = mmrGain_range.pop()
            if mmrGain_min <= mmrGain:
                return mmrGain_min
        return "~0"

    def split_tier(self, mmrBefore, mmrGain):
        mmrBefore_range = [0, 1000, 2000, 3000, 4000, 5000, 6000]
        mmrGain_range = self._split_mmrGain(mmrGain)
        self.tier["all"][mmrGain_range] = self.tier["all"].get(mmrGain_range, 0) + 1
        while mmrBefore_range:
            tier_min = mmrBefore_range.pop()
            if tier_min <= mmrBefore:
                self.tier[tier_range[tier_min]][mmrGain_range] = (
                    self.tier[tier_range[tier_min]].get(mmrGain_range, 0) + 1
                )
                break

    def mean(self):
        tiers = self.tier
        for tier in tiers:
            tier_values = tiers[tier]
            total = sum(tier_values.values())
            self.total[tier] = total
            for tier_value in tier_values:
                tier_values[tier_value] /= total


class Re_Tier:
    def __init__(self):
        self.tier = {}
        self.tier["아이언"] = {}
        self.tier["브론즈"] = {}
        self.tier["실버"] = {}
        self.tier["골드"] = {}
        self.tier["플레티넘"] = {}
        self.tier["다이아"] = {}
        self.tier["데미갓"] = {}
        self.tier["all"] = {}
        self.total = {}

    def split_tier(self, mmrBefore, condition):
        mmrBefore_range = [0, 1000, 2000, 3000, 4000, 5000, 6000]
        # mmrGain_range = self._add_data(condition)
        # self.tier["all"][mmrGain_range] = self.tier["all"].get(mmrGain_range, 0) + 1
        while mmrBefore_range:
            tier_min = mmrBefore_range.pop()
            if tier_min <= mmrBefore:
                self._add_Data(tier_min, mmrBefore)
                # self.tier[tier_range[tier_min]][mmrGain_range] = (
                #     self.tier[tier_range[tier_min]].get(mmrGain_range, 0) + 1
                # )
                break

    def _add_Data(self, tier, mmrGain):
        mmrGain_range = [0, 25, 50, 75, 100, 125, 150, 175, 200, 225]
        while mmrGain_range:
            mmrGain_min = mmrGain_range.pop()
            if mmrGain_min <= mmrGain:
                return mmrGain_min
        return "~0"
