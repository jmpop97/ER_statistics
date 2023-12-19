from pymongo import MongoClient
from glob import glob
import json
from .cryption_secret import AESCipher
import requests
import time
from ..ER_apis.ER_api import request_to_ER_api

NORMAL_MODE_NUMBER = 2
RANK_MODE_NUMBER = 3
COBALT_MODE_NUMBER = 6
OK_RESPONSE = 200
SEASON_ID = 21

def get_mongoDB_connection_string():
    with open("setting/secret_db.json", "r", encoding="utf-8") as f:
        db_url = json.load(f)
    CRYPTION_KEY = "KEYFORDB"
    aes = AESCipher(CRYPTION_KEY)
    RW_EC2_DB_CONNECTION_STRING = aes.decrypt(db_url["EC2_DB_CONNECTION_STRING"])
    READ_EC2_DB_CONNECTION_STRING = aes.decrypt(db_url["READ_EC2_DB_CONNECTION_STRING"])
    return RW_EC2_DB_CONNECTION_STRING, READ_EC2_DB_CONNECTION_STRING


def access_RW_mongoDB() -> MongoClient:
    RW_DB_CONNECTION_STRING = get_mongoDB_connection_string()[0]
    client = MongoClient(RW_DB_CONNECTION_STRING, port=27017)
    return client


def access_read_mongoDB() -> MongoClient:
    READ_DB_CONNECTION_STRING = get_mongoDB_connection_string()[3]
    client = MongoClient(READ_DB_CONNECTION_STRING, port=27017)
    return client


def insert_game_play_datas_local_to_mongoDB() -> None:
    client = access_RW_mongoDB()
    access_db = client["ERDB"]
    collection = access_db["game_play_datas"]

    game_list = glob("./datas/Ver*.*.json")
    inserted_file_cnt = 0
    for file_name in game_list:
        with open(file_name, "r", encoding="utf-8") as f:
            file_data = json.load(f)
        file_data["_id"] = file_data["userGames"][0]["gameId"]
        inserted_id = collection.insert_one(file_data).inserted_id
        inserted_file_cnt += 1
        print(
            "id: {0} filename: {1} {2}/{3}".format(
                inserted_id, file_name, inserted_file_cnt, len(game_list)
            )
        )
    client.close()

def get_recent_game_id_from_ranker()->int:
    recent_game_id = None
    responced_current_ranker_data = request_to_ER_api(request_url=f"https://open-api.bser.io/v1/rank/top/{SEASON_ID}/{RANK_MODE_NUMBER}")
    if responced_current_ranker_data==None:
        print('error')
        return None
    ranker_user_num = responced_current_ranker_data["userGames"][0]["userNum"]
    responced_ranker_game_match_data = request_to_ER_api(request_url=f"https://open-api.bser.io/v1/user/games/{ranker_user_num}")
    if responced_ranker_game_match_data==None:
        print("error from no game id")
        return None
    recent_game_id =  responced_ranker_game_match_data['userGames'][0]['gameId']
    return recent_game_id

# insert game_match_data document to mongoDB directly by using ER API
def insert_game_play_datas_mongoDB(
    from_game_id: int, game_numbers_to_save: int
) -> None:
    client = access_RW_mongoDB()
    access_db = client["ERDB"]
    collection = access_db["game_play_datas"]
    with open("setting/secret.json", "r", encoding="utf-8") as f:
        token = json.load(f)
    headerDict = {}
    headerDict.setdefault("x-api-key", token["token"])
    inserted_file_cnt = 0
    to_game_id = from_game_id + game_numbers_to_save
    to_save_game_id_list = range(from_game_id, to_game_id)
    for game_id in to_save_game_id_list:
        requestDataWithHeader = requests.get(
            f"https://open-api.bser.io/v1/games/{game_id}", headers=headerDict
        )
        responced_game_match_data = requestDataWithHeader.json()
        if responced_game_match_data.get("code", 0) == OK_RESPONSE:
            responced_game_match_data["_id"] = responced_game_match_data["userGames"][
                0
            ]["gameId"]
            inserted_id = collection.insert_one(responced_game_match_data).inserted_id
            inserted_file_cnt += 1
            print(
                "id: {0} ({1}/{2})".format(
                    inserted_id, inserted_file_cnt, len(to_save_game_id_list)
                )
            )
            time.sleep(1)
        else:
            print("ERROR: responced code not 200")
            print(
                "game_id: {0}\tcode: {1}".format(
                    game_id, responced_game_match_data.get("code")
                )
            )
            continue
    client.close()
    print("[[insert end]]")


def get_lowest_id() -> int:
    client = access_read_mongoDB()
    collection = client["ERDB"]["game_play_datas"]
    lowest_id_document = collection.find_one({}, sort=[("_id", 1)])
    client.close()
    if lowest_id_document:
        return lowest_id_document["_id"]
    else:
        return None


def get_highest_id() -> int:
    client = access_read_mongoDB()
    collection = client["ERDB"]["game_play_datas"]
    highest_id_document = collection.find_one({}, sort=[("_id", -1)])
    client.close()
    if highest_id_document:
        return highest_id_document["_id"]
    else:
        return None


def get_all_match_datas_from_mongoDB() -> list:
    client = access_read_mongoDB()
    collection = client["ERDB"]["game_play_datas"]
    game_match_data_list = collection.find()
    client.close()
    for game_match_data in game_match_data_list:
        print(game_match_data["userGames"][0]["gameId"])
    return game_match_data_list


def show_all_match_datas_from_mongoDB() -> list:
    client = access_read_mongoDB()
    collection = client["ERDB"]["game_play_datas"]
    game_match_data_list = collection.find()
    client.close()
    for game_match_data in game_match_data_list:
        print(game_match_data["userGames"][0]["gameId"])


def query_mongoDB(query_list: list) -> list:
    client = access_read_mongoDB()
    collection = client["ERDB"]["game_play_datas"]
    game_match_data_list = []
    for query in query_list:
        queried_game_match_data_list: list = collection.find(query)
        game_match_data_list += queried_game_match_data_list
        print("loaded game play from DB")
    client.close()
    return game_match_data_list


def delete_old_documents(from_game_id: int, delete_number: int):
    client = access_RW_mongoDB()
    collection = client["ERDB"]["game_play_datas"]
    try:
        documents_to_delete = collection.find({"_id": {"$gte": (from_game_id)}}).limit(
            delete_number
        )
        result = collection.delete_many(
            {"_id": {"$in": [doc["_id"] for doc in documents_to_delete]}}
        )
        print(f"{result.deleted_count} documents deleted.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        client.close()


def create_query_version(
    major_version: int,
    minor_version: int,
    game_mode_list: list = ["Rank"],
    min_players: int = 18,
) -> list:
    game_mode_num_list = translate_game_mode_str_to_int(game_mode_list)

    query_list = []
    for game_mode_num in game_mode_num_list:
        query = {
            "userGames.versionMajor": major_version,
            "userGames.versionMinor": minor_version,
            "userGames.matchingMode": game_mode_num,
            "userGames." + str(min_players): {"$exists": True},
        }
        if game_mode_num == COBALT_MODE_NUMBER:
            query.pop("userGames." + str(min_players), None)
        query_list.append(query)
    return query_list


def create_query_gameId(
    from_game_id: int,
    to_game_id: int,
    game_mode_list: list = ["Rank"],
    min_players: int = 18,
) -> list:
    game_mode_num_list = translate_game_mode_str_to_int(game_mode_list)

    query_list = []
    for game_mode_num in game_mode_num_list:
        query = {
            "_id": {"$gte": from_game_id, "$lte": to_game_id},
            "userGames.matchingMode": game_mode_num,
            "userGames." + str(min_players): {"$exists": True},
        }
        if game_mode_num == COBALT_MODE_NUMBER:
            query.pop("userGames." + str(min_players), None)
        query_list.append(query)
    return query_list


def translate_game_mode_str_to_int(input_game_mode_list: list):
    game_mode_num_list = []
    for game_mode in input_game_mode_list:
        if game_mode == "Normal":
            game_mode_num_list.append(NORMAL_MODE_NUMBER)
        elif game_mode == "Rank":
            game_mode_num_list.append(RANK_MODE_NUMBER)
        elif game_mode == "Cobalt":
            game_mode_num_list.append(COBALT_MODE_NUMBER)
    return game_mode_num_list
