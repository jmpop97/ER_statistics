import json

from .ER_api import save_games

import unittest

class SaveGames(unittest.TestCase):
    def test_save_game(self):
        with open("./datas/Ver9.0_Rank_31131392.json", "r", encoding="utf-8") as f:
            game_datas = json.load(f)
        self.assertTrue(game_datas.get("code", 0) == 200)
