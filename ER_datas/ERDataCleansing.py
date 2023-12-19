import os

os.system("cls")
from ER_datas.data_class import DataClass
from .rank_mmr import mmr_charges
from .tier_mmr import Tier
from ER_apis.ER_DB import query_mongoDB, create_query_version

# game_data 가져오기


import json
from glob import glob

major_version, minor_version = -1, -1


def load_lastest_version():
    game_list = sorted(glob("./datas/Ver*.json"))
    last_game = (game_list[-1].split("Ver")[1]).split("._")[0]
    lastest_version = last_game.split("_")[0]
    print(lastest_version)
    return lastest_version.split(".")[0], lastest_version.split(".")[1]


def load_lastest_verson_from_file():
    file_name = "./setting/game_version.json"
    with open(file_name, "r", encoding="utf-8") as f:
        lastest_version = json.load(f)
    return (
        lastest_version["CURRENT_GAME_MAJOR_VERSION"],
        lastest_version["CURRENT_GAME_MINOR_VERSION"],
    )


# game_mode ["Rank", "Normal"]
# "Rank"
#
def ERDataCleansing(
    data_class=DataClass(), game_mode: list = ["Rank"], DB_type: str = ""
) -> None:
    if not DB_type:
        if major_version == -1 and minor_version == -1:
            major_version, minor_version = load_lastest_verson_from_file()
        elif major_version == -1 or minor_version == -1:
            print("version error,used base Version")

    for mode in game_mode:
        if DB_type == "EC2":
            major_version, minor_version = load_lastest_verson_from_file()
            query = create_query_version(
                majorVersion=major_version,
                minorVersion=minor_version,
                game_mode=game_mode,
            )
            game_list = query_mongoDB(query_list=query)
            for game_datas in game_list:
                for user_data in game_datas["userGames"]:
                    """유저 정보"""
                    data_class.add_data(user_data)
                data_class.add_data_game_id()
        elif DB_type == "test":
            game_list = [
                "./datas/Ver9.0_Rank_31130633.json",
                "./datas/Ver9.0_Rank_31131392.json",
            ]
        else:
            game_list = glob(
                "./datas/Ver{0}.{1}_{2}_*.json".format(
                    major_version, minor_version, mode
                )
            )
        for file_name in game_list:
            with open(file_name, "r", encoding="utf-8") as f:
                game_datas = json.load(f)
            # file_index = str(file_name.split("_")[2]).split(".")[0]
            # print("Add {0}.json".format(file_index))
            for user_data in game_datas["userGames"]:
                """유저 정보"""
                data_class.add_data(user_data)
            data_class.add_data_game_id()
        data_class.last_calculate()
