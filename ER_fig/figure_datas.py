import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np
import seaborn as sns
from ER_datas.data_class import *
from ER_datas.ERDataCleansing import ERDataCleansing
from ER_datas.id_characterName import LoadCharacter
import json

plt.rcParams["font.family"] = "Malgun Gothic"
plt.rcParams["axes.unicode_minus"] = False


dic_characterNum_Name = LoadCharacter()


def plot_set_data(plt, data, condition):
    x_type = condition[0]
    y_type = condition[1]
    plt.plot(data[x_type], data[y_type], "o")
    plt.xlabel(x_type, labelpad=10)
    plt.ylabel(y_type, labelpad=10)
    # plt.plot(mmr_ranges,mmr_lines,'r')
    plt.subplots_adjust(left=0.07, bottom=0.06, top=0.9)


from ER_datas.rank_mmr import mmr_line


def plot_mmrcharge_set_data(plt, data, condition):
    x_type = condition[0]
    y_type = condition[1]
    plt.plot(data[x_type], data[y_type], "o")
    plt.xlabel(x_type, labelpad=10)
    plt.ylabel(y_type, labelpad=10)
    figure_red = mmr_line()
    plt.plot(figure_red[x_type], figure_red[y_type], "r")
    plt.subplots_adjust(left=0.07, bottom=0.06, top=0.9)


dic_figureType_setData = {
    "plot": plot_set_data,
    "plot_mmrcharge": plot_mmrcharge_set_data,
}


def figure_save(dic_datas, figure_type, condition):
    for i in dic_characterNum_Name:
        # 한글화
        i = int(i)
        datas = dic_datas.dic_characterNum_datas.get(i, {})
        if datas == {}:
            continue
        plt.rcParams["font.family"] = "Malgun Gothic"
        plt.style.use("_mpl-gallery")
        mpl.rcParams["axes.unicode_minus"] = False
        # 그래프 이름과 사이즈
        plt.figure(i, figsize=(10, 6))
        plt.title(dic_characterNum_Name[str(i)], pad=10)
        plt.savefig("fig/" + dic_characterNum_Name[str(i)] + "mmr_mmrGain")

        # 데이터 설정
        dic_figureType_setData[figure_type](plt, datas, condition)
        # 그래프 보기
        plt.show()
        # figure삭제
        plt.cla()  # clear the current axes
        plt.clf()  # clear the current figure
        plt.close()  # closes the current figure


class FigureType:
    def __init__(self, bool_save=False, bool_show=True):
        self.plt = plt
        self.bool_save = bool_save
        self.bool_show = bool_show

    def scatterplot(
        self, db, x_type, y_type, titles="", team_color="red", figure_n=1, s=1
    ):
        plts = self.plt
        plts.figure(figure_n)
        plts.title(titles)
        plts.xlabel(x_type)
        plts.ylabel(y_type)
        plts.scatter(
            db[x_type], db[y_type], color=team_color, s=s
        )  # 산포도 그래프 호출: scatter(x, y)

    def bar_graph_n(
        self, db={}, titles="", bar_count=1, bar_num=1, team_color="red", figure_n=2
    ):
        alpha = 0.5  # 1/bar_count
        bar_width = 0.7 / bar_count
        plts = self.plt
        plts.figure(figure_n)
        plts.title(titles)
        x = np.arange(len(db))
        plts.bar(
            x + (bar_num - 1) * bar_width,
            db.values(),
            bar_width,
            alpha=alpha,
            color=team_color,
        )
        # plts.xticks(x,db.keys())

    def bar_graph_one(
        self, db={}, titles="", bar_count=1, bar_num=1, team_color="red", figure_n=2
    ):
        db_list = db.items()
        x, y = zip(*db_list)
        alpha = 0.5  # 1/bar_count
        bar_width = 0.7 / bar_count
        plt.bar(x, y, bar_width, alpha=alpha, color=team_color)

    def bar_graph_all(
        self,
        db1={},
        db2={},
        db3={},
        db4={},
        titles="",
        bar_count=1,
        bar_num=1,
        team_color="red",
        figure_n=2,
    ):
        db1_list = db1.items()
        x1, y1 = zip(*db1_list)
        db2_list = db2.items()
        x2, y2 = zip(*db2_list)
        db3_list = db3.items()
        x3, y3 = zip(*db3_list)
        db4_list = db4.items()
        x4, y4 = zip(*db4_list)
        alpha = 0.5  # 1/bar_count
        bar_width = 0.7 / bar_count
        plt.figure(1)
        plt.bar(x1, y1, bar_width, alpha=alpha, color=team_color)
        plt.figure(2)
        plt.bar(x2, y2, bar_width, alpha=alpha, color=team_color)
        plt.figure(3)
        plt.bar(x3, y3, bar_width, alpha=alpha, color=team_color)
        plt.figure(4)
        plt.bar(x4, y4, bar_width, alpha=alpha, color=team_color)

    def show(self):
        self.plt.show()

    def save(self, name="error"):
        self.plt.savefig("fig/" + name)

    def clear(self):
        self.plt.cla()  # clear the current axes
        self.plt.clf()  # clear the current figure
        self.plt.close()  # closes the current figure

    def save_show(self, name="error", save=None, show=None):
        if save != None:
            self.bool_save = save
        if show != None:
            self.bool_show = show

        if self.bool_show:
            self.show()
        if self.bool_save:
            self.save(name)
        self.clear()

    def lineplot(self, figure_n=1, **coditions):
        plts = self.plt
        plts.figure(figure_n)
        plts.set_facecolor("white")
        sns.lineplot(**coditions)

    def barplot(self, figure_n=1, **coditions):
        plts = self.plt
        plts.figure(figure_n)
        sns.barplot(**coditions)

    def title(self, condition):
        self.plt.title(condition)


class TierGetMMR:
    fig_size_x = 13
    fig_zise_y = 6
    font_size = 6

    def __init__(self) -> None:
        dic_name = {"mmrBefore//250": "Tier"}
        self.db = ListFilterData(
            "gameRank", "mmrGainInGame", "mmrBefore//250", **dic_name
        )
        ERDataCleansing(self.db)

        self.tier_cost = []
        self.tier = []

    def plt(self):
        self._tier_get_mmr()
        self._tier_cost_red_line()
        self._tier_line()
        self._countplot()
        self._tier_line()
        plt.show()

    def _tier_get_mmr(self):
        plt.figure(1, figsize=(self.fig_size_x, self.fig_zise_y))
        ax = sns.barplot(data=self.db.conditions, y="mmrGainInGame", x="Tier")
        ax.bar_label(ax.containers[0], fontsize=self.font_size)

    def _tier_cost_red_line(self):
        self._tier_cost()
        plt.plot(self.tier, self.tier_cost, "r")

    def _tier_line(self):
        line = 3.5
        while line < self.tier[-1]:
            plt.axvline(x=line, color="r", linestyle="--", linewidth=1)
            line += 4

    def _tier_cost(self):
        with open("./base_datas/TierMMRCost/TierMMRCost.json", "r") as f:
            tier_cost = json.load(f)
        for tier in sorted(set(self.db.conditions["Tier"])):
            self.tier_cost.append(tier_cost.get(str(tier), 2 * tier + 5))
            self.tier.append(tier)

    def _countplot(self):
        plt.figure(2, figsize=(self.fig_size_x, self.fig_zise_y))
        ax = sns.countplot(data=self.db.conditions, x="Tier")
        ax.bar_label(ax.containers[0], fontsize=10)


class TierGetMMRFromRank:
    def __init__(self) -> None:
        self.db = GetMMRFromRank()
        ERDataCleansing(self.db)
        self.tier_cost = []
        self.tier = []

    def plt(self):
        self._barplot()
        self._tier_cost_red_line()
        plt.show()

    def _barplot(self):
        ax = sns.barplot(
            data=self.db.datas,
            x="Tier",
            y="mmrGainInGame",
            estimator="mean",
            order=self.db._tier.values(),
        )
        ax = sns.barplot(data=self.db.datas, x="Tier", y="mmrRank", estimator="mean")
        ax.bar_label(ax.containers[0], label_type="center")
        ax.bar_label(ax.containers[1], label_type="center")

    def _tier_cost_red_line(self):
        self._tier_cost()
        plt.plot(self.tier, self.tier_cost, "r")

    def _tier_cost(self):
        with open("./base_datas/TierMMRCost/TierMMRCost.json", "r") as f:
            tier_cost = json.load(f)
        for tier in self.db._tier:
            real_tier = tier * 4 + 3
            self.tier_cost.append(tier_cost.get(str(real_tier), 2 * real_tier + 5))
            self.tier.append(self.db._tier[tier])
