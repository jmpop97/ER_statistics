import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from ER_apis.ER_DB import get_lowest_id, delete_old_documents
import argparse

argument_parser = argparse.ArgumentParser()
argument_parser.add_argument(
    "--n", help="how many games to delete in mongoDB", type=int, default=500
)

# done
if __name__ == "__main__":
    lowest_id_in_mongoDB = get_lowest_id()
    if lowest_id_in_mongoDB == None:
        exit(1)
    delete_old_documents(
        from_game_id=lowest_id_in_mongoDB, delete_number=argument_parser.parse_args().n
    )
