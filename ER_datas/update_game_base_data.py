import json
import requests

SECRET_FILE_PATH = "./secret.json"
BASE_DATAS_PATH = "./base_datas/"
TXT_GAME_BASE_DATA_FILE_NAME = "game_base_data.txt"
JSON_GAME_BASE_DATA_FILE_NAME = "game_base_data.json"


def put_in_dictionary(list, d):
    """
    리스트가 존재할 때
    첫번째 인덱스일때에는 dictionary에 list[0]에 해당하는 딕셔너리 추가하기
    점차 재귀로 들어가야한다.
    """
    try:
        if d.get(list[0]) == None:
            if len(list) == 2:
                d[list[0]] = [list[1]]
            else:
                d[list[0]] = {}
                d[list[0]] = put_in_dictionary(list[1:], d[list[0]])
        else:
            if len(list) == 2:
                d[list[0]] = list[1]
            else:
                d[list[0]] = put_in_dictionary(list[1:], d[list[0]])
    except AttributeError as e:
        # list
        if len(list) == 2:
            d.append({list[0]: list[1]})
        else:
            temp_dictionary = {}
            put_in_dictionary(list[1:], temp_dictionary)
            # try:
            d.append(temp_dictionary)
            # except AttributeError as e2:
            #    d[list[0]].append()
            print("error name: ", e)
            print("dictionary: ", d)
            print("list: ", list)
    return d


def change_txt_to_json():
    game_data = {}
    with open(
        BASE_DATAS_PATH + TXT_GAME_BASE_DATA_FILE_NAME, "r", encoding="utf-8"
    ) as f:
        while True:
            line = f.readline()
            # txt파일 끝일 경우에는 이렇게 한다
            if line == "--xxxxxxxxxx--":
                break
            # txt파일 중간중간에 빈 줄이 존재하여 이렇게 작성
            if not line or line == "\n":
                continue
            key, value = line.split("┃")
            key_list = key.split("/")
            key_list.append(value[:-1])
            put_in_dictionary(key_list, game_data)
    return game_data


def save_updated_game_base_data(language="Korean"):
    url = "https://open-api.bser.io/v1/l10n/Korean/"
    with open(SECRET_FILE_PATH, "r", encoding="utf-8") as f:
        token = json.load(f)
    datas = {"x-api-key": token["token"], "language": language}
    response = requests.get(url, headers=datas)
    response_datas = response.json()

    if response_datas.get("code", 0) == 200:
        file_url = response_datas["data"]["l10Path"]
        file = requests.get(file_url)
        open(BASE_DATAS_PATH + TXT_GAME_BASE_DATA_FILE_NAME, "wb").write(file.content)


def update_game_base_data(language="Korean"):
    save_updated_game_base_data(language)
    data = change_txt_to_json()
    with open(
        BASE_DATAS_PATH + JSON_GAME_BASE_DATA_FILE_NAME, "w", encoding="UTF-8-sig"
    ) as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

change_txt_to_json()