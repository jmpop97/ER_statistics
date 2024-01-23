import json

from .ER_api import (
    save_games,
    request_free_characters,
    request_to_ER_api,
    NORMAL_MODE_NUMBER,
)
import unittest


class SaveGames(unittest.TestCase):
    # ????
    def test_save_game(self):
        with open("./datas/Ver9.0_Rank_31131392.json", "r", encoding="utf-8") as f:
            game_datas = json.load(f)
        self.assertTrue(game_datas.get("code", 0) == 200)

    def test_request_to_ER_api(self):
        save_result = request_to_ER_api(
            request_url=f"https://open-api.bser.io/v1/freeCharacters/{NORMAL_MODE_NUMBER}"
        )
        self.assertTrue(save_result != None)

    def test_request_free_characters(self):
        self.assertTrue(request_free_characters())
