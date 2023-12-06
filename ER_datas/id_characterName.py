import json


def LoadCharacter():
    file_name = "./base_datas/game_base_data.json"
    with open(file_name, "rt", encoding="utf-8-sig") as f:
        file_data = json.load(f)
    character_name = file_data["Character"]["Name"]
    return character_name
