import json

from .ER_api import ERAPI
import unittest
from dotenv import load_dotenv
import os
from public_setting.variable import GameType
load_dotenv()

class SaveGames(unittest.TestCase):
    def test_request_to_ER_api(self):
        # ERAPI().save_games(33240713,duplication=False)
        pass
    '''
    
    def test_request_region_rankers_eternity_cut(self):
        responced_data = request_region_rankers_eternity_cut()
        self.assertTrue(responced_data != None)
    '''