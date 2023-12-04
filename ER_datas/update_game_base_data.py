import json
import requests

SECRET_FILE_PATH = "./secret.json"
BASE_DATAS_PATH = "./base_datas/"
TXT_GAME_BASE_DATA_FILE_NAME = "game_base_data.txt"
JSON_GAME_BASE_DATA_FILE_NAME = "game_base_data.json"


def put_in_dictionary(input_list, d):
    """
    리스트가 존재할 때
    첫번째 인덱스일때에는 dictionary에 input_list[0]에 해당하는 딕셔너리 추가하기
    점차 재귀로 들어가야한다.
    """
    try:
        if d.get(input_list[0]) == None:
            if len(input_list) == 2:
                d[input_list[0]] = [input_list[1]]
            else:
                d[input_list[0]] = {}
                d[input_list[0]] = put_in_dictionary(input_list[1:], d[input_list[0]])
        else:
            if len(input_list) == 2:
                d[input_list[0]] = input_list[1]
            else:
                d[input_list[0]] = put_in_dictionary(input_list[1:], d[input_list[0]])
    except AttributeError as e:
        # input_list
        if len(input_list) == 2:
            d.append({input_list[0]: input_list[1]})
        else:
            temp_dictionary = {}
            put_in_dictionary(input_list[1:], temp_dictionary)
            # try:
            # if type(d)==dict:
            if type(d) == list:
                d.append(temp_dictionary)
            elif type(d) == dict:
                key = input_list[0]
                d[key] = temp_dictionary
            else:
                d.append(temp_dictionary)

            # except AttributeError as e2:
            #    d[input_list[0]].append()
            print("error name: ", e)
            print("dictionary: ", d)
            print("input_list: ", input_list)
    return d


def cleanDictionary(input_key_list, output_dict):
    while input_key_list:
        if type(output_dict[input_key_list[0]]) == list:
            if len(output_dict[input_key_list[0]]) == 1:
                output_dict[input_key_list[0]] = output_dict[input_key_list[0]][0]
        elif type(output_dict[input_key_list[0]]) == dict:
            next_key_list = list(output_dict[input_key_list[0]].keys())
            cleanDictionary(next_key_list, output_dict[input_key_list[0]])
        elif type(output_dict[input_key_list[0]]) == str:
            input_key_list.pop(0)
            continue
        else:
            print("error")
            exit(1)
        input_key_list.pop(0)
    return output_dict


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
    data = cleanDictionary(list(data.keys()), data)
    with open(
        BASE_DATAS_PATH + JSON_GAME_BASE_DATA_FILE_NAME, "w", encoding="UTF-8-sig"
    ) as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


update_game_base_data()
