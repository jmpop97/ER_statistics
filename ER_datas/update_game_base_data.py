import json
import requests
import os

SECRET_FILE_PATH = "./setting/secret.json"
BASE_DATAS_PATH = "./base_datas"
ORIGIN_DATAS_PATH = "./origin_datas"
TXT_GAME_BASE_DATA_FILE_PATH = "./origin_datas/game_base_data.txt"
TXT_GAME_BASE_DATA_FILE_NAME = "game_base_data.txt"

'''
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
        ORIGIN_DATAS_PATH + TXT_GAME_BASE_DATA_FILE_PATH, "r", encoding="utf-8"
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
def update_game_base_data(language="Korean"):
    save_updated_game_base_data(language)
    data = change_txt_to_json()
    data = cleanDictionary(list(data.keys()), data)
    with open(
        BASE_DATAS_PATH + JSON_GAME_BASE_DATA_FILE_PATH, "w", encoding="UTF-8-sig"
    ) as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
def change_txt_to_base_files():
    with open(
        BASE_DATAS_PATH + "/" + TXT_GAME_BASE_DATA_FILE_PATH, "r", encoding="utf-8"
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
            key_list = keys.split("/")
            if len(key_list)==1:
                # others 파일 내부에 key:value로 넣기
                data={keys:value}
                filename = BASE_DATAS_PATH + "/others.json"
                if os.path.exists(filename):
                    appendDataTojsonFile(filename, data)
                else:
                    with open(
                        filename, "w", encoding="UTF-8-sig"
                    ) as write_file:
                        json.dump(data, write_file, indent=4, ensure_ascii=False)
            else:
                filepath = BASE_DATAS_PATH
                data = {key_list[-1]:value}
                for key in key_list[:-1]:
                    filepath=filepath+"/"+key
                    if key==key_list[-2]:
                        continue
                    if not os.path.exists(filepath):
                        os.makedirs(filepath)
                filename = filepath+".json"
                if os.path.exists(filename):
                    appendDataTojsonFile(filename, data)
                else:
                    with open(
                        filename, "w", encoding="UTF-8-sig"
                    ) as write_file:
                        json.dump(data, write_file, indent=4, ensure_ascii=False)
    return True
'''


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
