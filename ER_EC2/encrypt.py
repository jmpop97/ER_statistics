from ER_apis.cryption_secret import AESCipher
import argparse
import json

argument_parser = argparse.ArgumentParser()
argument_parser.add_argument("--w", help="connection url for read write DB role", type=str)
argument_parser.add_argument("--r", help="connection url for read only DB role", type=str)


if __name__=="__main__":
    CRYPTION_KEY = "KEYFORDB"
    aes = AESCipher(CRYPTION_KEY)
    READ_DB_CONNECTION_STRING = argument_parser.parse_args().r
    RW_DB_CONNECTION_STRING = argument_parser.parse_args().w
    EC2_DB_CONNECTION_STRING=aes.encrypt(READ_DB_CONNECTION_STRING)
    RW_DB_CONNECTION_STRING=aes.encrypt(RW_DB_CONNECTION_STRING)
    db_connection_url_dictionary = {
        "EC2_DB_CONNECTION_STRING":EC2_DB_CONNECTION_STRING,
        "RW_DB_CONNECTION_STRING":RW_DB_CONNECTION_STRING
    }
    with open("setting/secret_db.json", "w") as write_file:
        json.dump(db_connection_url_dictionary, write_file, indent="\t")
