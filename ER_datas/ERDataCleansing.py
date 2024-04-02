import os

os.system("cls")
from ER_datas.data_class import DataClass
from .rank_mmr import mmr_charges
from ER_apis.ER_DB import query_mongoDB, create_query_version
from public_setting.variable import GameDB, GameVerson
from dotenv import load_dotenv
from public_setting.function import createfile
import asyncio

# game_data 가져오기

load_dotenv()
import json
from glob import glob


def load_lastest_version():
    game_list = sorted(glob("./datas/Ver*.json"))
    last_game = (game_list[-1].split("Ver")[1]).split("._")[0]
    lastest_version = last_game.split("_")[0]
    print(lastest_version)
    return lastest_version.split(".")[0], lastest_version.split(".")[1]


def load_lastest_verson_from_file():
    file_name = "setting/game_version.json"
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
    data_class=DataClass(),
    game_mode=["Rank"],
    DB_type: str = "",
    major_version: int = -1,
    minor_version: int = -1,
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
                "./handmadeDB/testcase/Ver9.0_Rank_31130633.json",
                "./handmadeDB/testcase/Ver9.0_Rank_31131392.json",
            ]
            print("test")
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
                data_class.user_count()
            data_class.add_data_game_id()
            data_class.game_count()
        data_class.last_calculate()
        print("유저 : ", data_class.user_count_num)
        print("게임 : ", data_class.game_count_num)


class ERDataCleansing:
    def __init__(
        self,
        data_class=DataClass(),
        game_mode=["Rank"],
        DB_type: str = "",
        major_version: int = -1,
        minor_version: int = -1,
    ) -> None:
        game_verson = GameVerson()
        major_version, minor_version = game_verson.major, game_verson.minor
        root_dir = os.environ.get("DB_DIR")

        if DB_type == "test":
            game_list = glob("./handmadeDB/testcase/*")
        else:
            game_list = GameDB(
                types=game_mode,
                major_version=[major_version],
                minor_version=[minor_version],
                root_dir=root_dir,
            ).dir_list

        for file_name in game_list:
            with open(file_name, "r", encoding="utf-8") as f:
                game_datas = json.load(f)
            # file_index = str(file_name.split("_")[2]).split(".")[0]
            # print("Add {0}.json".format(file_index))
            for user_data in game_datas["userGames"]:
                """유저 정보"""
                data_class.add_data(user_data)
                data_class.user_count()
            data_class.add_data_game_id()
            data_class.game_count()
        data_class.last_calculate()
        print("유저 : ", data_class.user_count_num)
        print("게임 : ", data_class.game_count_num)

        pass


class ASYNC_ERDataCleansing:
    """데이터 혼동의 오류가 존재 가능함
    특히 팀단위와 게임단위 작업시 위험
    왠만하면 단순 데이터 필터링에서만 쓰자"""

    def __init__(
        self,
        data_class=DataClass(),
        game_mode=["Rank"],
        DB_type: str = "",
        major_version: int = -1,
        minor_version: int = -1,
    ) -> None:
        game_verson = GameVerson()
        major_version, minor_version = game_verson.major, game_verson.minor
        root_dir = os.environ.get("DB_DIR")

        if DB_type == "test":
            game_list = glob("./handmadeDB/testcase/*")
        else:
            game_list = GameDB(
                types=game_mode,
                major_version=[major_version],
                minor_version=[minor_version],
                root_dir=root_dir,
            ).dir_list

        # for file_name in game_list:
        asyncio.run(read_all_datas(game_list, data_class))

        data_class.last_calculate()
        print("유저 : ", data_class.user_count_num)
        print("게임 : ", data_class.game_count_num)

        pass


async def add_game_id(dir, data_class: DataClass):
    with open(dir, "r", encoding="utf-8") as f:
        game_datas = json.load(f)
    for user_data in game_datas["userGames"]:
        data_class.add_data(user_data)
        data_class.user_count()
    data_class.add_data_game_id()
    data_class.game_count()


async def read_all_datas(dirs, data_class):
    await asyncio.wait(
        [asyncio.create_task(add_game_id(dir, data_class)) for dir in dirs]
    )
    print("end read data")
