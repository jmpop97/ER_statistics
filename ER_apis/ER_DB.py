from pymongo import MongoClient
import pymongo
from glob import glob
import json
from .cryption_secret import AESCipher

def getAccount():
    with open("secret_db.json", "r", encoding="utf-8") as f:
        db_url = json.load(f)
    CRYPTION_KEY="KEYFORDB"
    aes =AESCipher(CRYPTION_KEY)
    DB_CONNECTION_STRING=aes.decrypt(db_url['DB_CONNECTION_STRING'])
    READ_DB_CONNECTION_STRING=aes.decrypt(db_url['READ_DB_CONNECTION_STRING'])
    return DB_CONNECTION_STRING, READ_DB_CONNECTION_STRING

def access_RW_mongoDB():
    DB_CONNECTION_STRING = getAccount()[0]
    client = MongoClient(DB_CONNECTION_STRING)
    access_db = client['ERDB']
    collection= access_db["game_play_datas"]
    return collection

def access_mongoDB():
    READ_DB_CONNECTION_STRING = getAccount()[1]
    client = MongoClient(READ_DB_CONNECTION_STRING)
    access_db = client['ERDB']
    collection= access_db["game_play_datas"]
    return collection

def update_mongoDB():
    collection= access_RW_mongoDB()
    game_list = glob("./datas/Ver*.*.json")
    for file_name in game_list:
        with open(file_name, "r", encoding="utf-8") as f:
            file_data = json.load(f)
        collection.insert_one(file_data)

def get_all_match_datas_from_mongoDB():
    collection= access_mongoDB()
    items = collection.find()
    '''
    for item in items:
        print(item['userGames'][0]['gameId'])
    '''
    return items

def query_mongoDB(query_list):
    collection=access_mongoDB()
    items=[]
    for query in query_list:
        datas=collection.find(query)
        item_list = list(datas)
        items =items + item_list
    '''
    for item in items:
        print(item['userGames'][0]['gameId'])
    '''
    return items

def create_query_version(majorVersion, minorVersion, game_mode=["Rank"], min_players=18):
    modes=[]
    for mode in game_mode:
        if mode=="Normal":
            modes.append(2)
        elif mode=="Rank":
            modes.append(3)
        elif mode=="Cobalt":
            modes.append(6)

    query_list=[]
    for mode in modes:
        query= {"userGames.versionMajor":majorVersion, 
                 "userGames.versionMinor":minorVersion, 
                 "userGames.matchingMode":mode, 
                 "userGames."+str(min_players):{"$exists":True}
                }
        if mode==6:
            query.pop("userGames."+str(min_players), None)
        query_list.append(query)
    return query_list

def create_query_gameId(fromGameId, toGameId, game_mode=["Rank"], min_players=18):
    modes=[]
    for mode in game_mode:
        if mode=="Normal":
            modes.append(2)
        elif mode=="Rank":
            modes.append(3)
        elif mode=="Cobalt":
            modes.append(6)

    query_list=[]
    for mode in modes:        
        query = {"userGames.gameId":{"$gte":fromGameId, "$lte":toGameId}, 
                  "userGames.matchingMode":mode, 
                  "userGames."+str(min_players):{"$exists":True}
                }
        if mode==6:
            query.pop("userGames."+str(min_players), None)
        query_list.append(query)
    return query_list