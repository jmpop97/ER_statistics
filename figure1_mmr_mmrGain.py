from ER1_mmr_datas import *

# 통계분석
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np


characterNumber = len(characterNum_dic)

from mmr_range import mmr_charges, mmr_line

mmr_ranges, mmr_lines = mmr_line()


"""입장료 제외하고 얻은 점수"""
for i in characterNum_dic:
    x = []
    y = []
    for mmrBefore in globals()["mmrBefore_datas" + str(i)]:
        for mmrBefore_datas in globals()["mmrBefore_datas" + str(i)][mmrBefore]:
            x += [mmrBefore]
            y += [mmrBefore_datas["mmrGain"] + mmr_charges(mmrBefore)]

    # size and color:

    # plot
    plt.rcParams["font.family"] = "Malgun Gothic"
    plt.style.use("_mpl-gallery")
    mpl.rcParams["axes.unicode_minus"] = False
    plt.figure(i, figsize=(10, 6))
    plt.plot(x, y, "o")
    plt.title(character_name[str(i)], pad=10)
    plt.xlabel("mmrBefore", labelpad=10)
    plt.ylabel("mmrGet", labelpad=10)
    plt.plot(mmr_ranges, mmr_lines, "r")
    plt.subplots_adjust(left=0.07, bottom=0.06, top=0.9)
    plt.savefig("fig/" + character_name[str(i)] + "mmr_mmrGain")
    plt.cla()  # clear the current axes
    plt.clf()  # clear the current figure
    plt.close()  # closes the current figure
