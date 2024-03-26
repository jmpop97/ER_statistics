import json
import os
from dotenv import load_dotenv

load_dotenv()


def LoadCharacter():
    with open("./base_datas/Character/Name.json", "rt", encoding="utf-8-sig") as f:
        character_name = json.load(f)
    return character_name
