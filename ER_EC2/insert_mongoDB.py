import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from ER_apis.ER_DB import insert_game_play_datas_mongoDB, get_highest_id, get_recent_game_id_from_ranker
import argparse

argument_parser = argparse.ArgumentParser()
argument_parser.add_argument("--n", help="GameNumbersToSave", type=int, default=1000)

if __name__ == "__main__":
    highest_game_id_in_DB = get_highest_id()
    recent_game_id_from_top_ranker = get_recent_game_id_from_ranker()
    print("highest_game_id_in_DB: ",highest_game_id_in_DB)
    print("recent_game_id_from_top_ranker: ",recent_game_id_from_top_ranker)
    from_game_id=recent_game_id_from_top_ranker
    game_numbers_to_save=argument_parser.n
    if (highest_game_id_in_DB >= recent_game_id_from_top_ranker+game_numbers_to_save):
        # here
        from_game_id = 1
    insert_game_play_datas_mongoDB(
        
    )
