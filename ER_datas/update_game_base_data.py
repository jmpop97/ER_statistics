import json
import requests
import os

SECRET_FILE_PATH = "./secret.json"
BASE_DATAS_PATH = "./base_datas/"
TXT_GAME_BASE_DATA_FILE_NAME = "game_base_data2.txt"
JSON_GAME_BASE_DATA_FILE_NAME = "game_base_data2.json"
SECRET_FILE_PATH = "./setting/secret.json"
BASE_DATAS_PATH = "./base_datas"
ORIGIN_DATAS_PATH = "./origin_datas"
TXT_GAME_BASE_DATA_FILE_PATH = "origin_datas/game_base_data.txt"
TXT_GAME_BASE_DATA_FILE_NAME = "game_base_data.txt"


def put_in_dictionary(list, d):
    """
    리스트가 존재할 때
    첫번째 인덱스일때에는 dictionary에 list[0]에 해당하는 딕셔너리 추가하기
    점차 재귀로 들어가야한다.
    """
    try:
        if d.get(list[0]) == None:
            if len(list) == 2:
                d[list[0]] = list[1]
            else:
                d[list[0]] = {}
                d[list[0]] = put_in_dictionary(list[1:], d[list[0]])
        else:
            if len(list) == 2:
                d[list[0]] = list[1]
            else:
                d[list[0]] = put_in_dictionary(list[1:], d[list[0]])
    except AttributeError as e:
        print(e)


def writeDataTojsonFile(filename, data):
    with open(filename, "w", encoding="UTF-8-sig") as target_file:
        json.dump(data, target_file, indent=4, ensure_ascii=False)
    target_file.close()


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
        if not os.path.exists(BASE_DATAS_PATH):
            os.mkdir(BASE_DATAS_PATH)
        open(TXT_GAME_BASE_DATA_FILE_PATH, "wb").write(file.content)


def change_txt_to_base_files():
    other_data = {}
    file_dict_data = {}
    with open(
        ORIGIN_DATAS_PATH + "/" + TXT_GAME_BASE_DATA_FILE_NAME, "r", encoding="utf-8"
    ) as f:
        while True:
            line = f.readline()
            # txt파일 끝일 경우에는 이렇게 한다
            if line == "--xxxxxxxxxx--":
                break
            # txt파일 중간중간에 빈 줄이 존재하여 이렇게 작성
            if not line or line == "\n":
                continue
            keys, value = line.split("┃")
            value = value[:-1]
            key_list = keys.split("/")
            # 이상한 case 발견...
            # <color=#F187E7>무료 </color>이벤트┃<color=#F187E7>무료 지급</color> 이벤트
            if len(key_list) > 1:
                range_size = list(range(len(key_list)))
                for i in range_size:
                    if key_list[i] == "":
                        key_list[i] = "None"
                        break
                    if key_list[i][-1] == "<":
                        key_list[i] = key_list[i] + "/" + key_list[i + 1]
                        key_list.pop(i + 1)
                        range_size.pop(-1)

            # others.json에 넣을 것
            if len(key_list) == 1:
                other_data[keys] = value
            # 폴더, 파일로 구분지을 것.
            else:
                filepath = BASE_DATAS_PATH
                data = {key_list[-1]: value}
                # key_list의 마지막 값은 json파일의 key값이 되어야한다.
                for index in range(len(key_list[:-1])):
                    filepath = filepath + "/" + key_list[index]
                    if index == len(key_list) - 2:
                        continue
                    if not os.path.exists(filepath):
                        os.makedirs(filepath)
                filename = filepath + ".json"
                if file_dict_data.get(filename) == None:
                    file_dict_data[filename] = [data]
                else:
                    file_dict_data[filename].append(data)
    return file_dict_data, other_data


def listToDict(input_list):
    return_dictionary = {}
    for element in input_list:
        return_dictionary.update(element)
    return return_dictionary


def write_dictionary_to_file(base_dict, other_data):
    # write base dictionary
    base_dict = dict(base_dict)
    for key in base_dict.keys():
        filepath = key
        write_dict = listToDict(base_dict[key])
        writeDataTojsonFile(filepath, write_dict)

    # write other data.json file
    other_data = dict(other_data)
    writeDataTojsonFile(BASE_DATAS_PATH + "/others.json", other_data)


def update_game_base_data(language="Korean"):
    save_updated_game_base_data(language)
    dictionary_data, others_data = change_txt_to_base_files()
    write_dictionary_to_file(dictionary_data, others_data)


class BaseDB:
    def __init__(self) -> None:
        self.origin_path = os.environ.get("BASE_DATAS_PATH")
        self.base_db_file_name = os.environ.get("TXT_GAME_BASE_DATA_FILE_NAME")
        self.change_txt_to_base_files()
        self.write_dictionary_to_file()

    def change_txt_to_base_files(self):
        other_data = {}
        file_dict_data = {}
        with open(
            ORIGIN_DATAS_PATH + "/" + TXT_GAME_BASE_DATA_FILE_NAME,
            "r",
            encoding="utf-8",
        ) as f:
            while True:
                line = f.readline()
                # txt파일 끝일 경우에는 이렇게 한다
                if line == "--xxxxxxxxxx--":
                    break
                # txt파일 중간중간에 빈 줄이 존재하여 이렇게 작성
                if not line or line == "\n":
                    continue
                keys, value = line.split("┃")
                value = value[:-1]
                key_list = keys.split("/")
                # 이상한 case 발견...
                # <color=#F187E7>무료 </color>이벤트┃<color=#F187E7>무료 지급</color> 이벤트
                if len(key_list) > 1:
                    range_size = list(range(len(key_list)))
                    for i in range_size:
                        if key_list[i] == "":
                            key_list[i] = "None"
                            break
                        if key_list[i][-1] == "<":
                            key_list[i] = key_list[i] + "/" + key_list[i + 1]
                            key_list.pop(i + 1)
                            range_size.pop(-1)

                # others.json에 넣을 것
                if len(key_list) == 1:
                    other_data[keys] = value
                # 폴더, 파일로 구분지을 것.
                else:
                    filepath = BASE_DATAS_PATH
                    data = {key_list[-1]: value}
                    # key_list의 마지막 값은 json파일의 key값이 되어야한다.
                    for index in range(len(key_list[:-1])):
                        filepath = filepath + "/" + key_list[index]
                        if index == len(key_list) - 2:
                            continue
                        if not os.path.exists(filepath):
                            os.makedirs(filepath)
                    filename = filepath + ".json"
                    if file_dict_data.get(filename) == None:
                        file_dict_data[filename] = [data]
                    else:
                        file_dict_data[filename].append(data)
        self.dict_data = file_dict_data
        self.other_data = other_data

    def write_dictionary_to_file(self):
        # write base dictionary
        base_dict = dict(self.dict_data)
        for key in base_dict.keys():
            filepath = key
            write_dict = listToDict(base_dict[key])
            writeDataTojsonFile(filepath, write_dict)

        # write other data.json file
        other_data = dict(self.other_data)
        writeDataTojsonFile(BASE_DATAS_PATH + "/others.json", other_data)
