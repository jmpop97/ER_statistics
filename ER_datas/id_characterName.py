import json

CHARACTER_FILE_NAME = "./base_datas/Character/Name.json"


def LoadCharacter():
    with open(CHARACTER_FILE_NAME, "rt", encoding="utf-8-sig") as f:
        character_name = json.load(f)
    return character_name
