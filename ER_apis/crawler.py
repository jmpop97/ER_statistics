import requests
import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pandas as pd
import time
from bs4 import BeautifulSoup
import pandas as pd
from public_setting.function import Json
import os

OK_RESPONSE = 404
REQUEST_CODES = "./setting/request_code.json"
CHROMEDRIVER_PATH = "/usr/src/chrome/chromedriver"
MAX_PAGE = 10


class Crawler:
    def __init__(
        self,
        param_dict: dict = {"teamMode": "SQUAD", "serverName": "seoul", "season": "11"},
    ):
        """
        if param_dict['season']=='':
            param_dict['season'] = get_latest_version_of_game()
        """
        # can be changed
        __user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        __options = webdriver.ChromeOptions()
        # options.add_argument('headless')
        __options.add_argument("--start-maximized")
        __options.add_argument("user-agent={0}".format(__user_agent))
        __options.add_argument("disable-gpu")
        self.__driver = webdriver.Chrome(options=__options)
        # https://dak.gg/er/leaderboard?teamMode=SQUAD&season=SEASON_11&serverName=seoul&page=10
        __base_url = "https://dak.gg/er/leaderboard"
        __url_param = (
            "?teamMode="
            + param_dict["teamMode"]
            + "&season=SEASON_"
            + param_dict["season"]
            + "&serverName="
            + param_dict["serverName"]
        )
        self.__crawling_url = __base_url + __url_param

        self.__eternity_players = []
        self.__demigod_players = []

    def crawling_top_players(self):
        for page_count in range(1, MAX_PAGE + 1):
            page_suffix = "&page=" + str(page_count)
            self.__driver.get(url=self.__crawling_url + page_suffix)
            try:
                WebDriverWait(driver=self.__driver, timeout=10).until(
                    EC.presence_of_element_located(
                        (By.CSS_SELECTOR, "#content-container > table")
                    )
                )
                columns = [
                    column_element.text
                    for column_element in self.__driver.find_elements(
                        By.XPATH, '//*[@id="content-container"]/table/thead/tr/th'
                    )
                ]
                df_players = pd.DataFrame(columns=columns)
                df_players = [
                    player_column.text.split("\n")[1:-3]
                    for player_column in self.__driver.find_elements(
                        By.XPATH, '//*[@id="content-container"]/table/tbody/tr'
                    )
                ]
                for player_data in df_players:
                    print(player_data)
            except TimeoutError as e:
                print("Time Exceeded")

        return df_players

    def __del__(self):
        self.__driver.quit()
        print("deleted")


class DakPlayerCrawler:
    def __init__(self, player_name, season):
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        options.add_argument("headless")
        options.add_argument("user-agent={0}".format(user_agent))
        options.add_argument("disable-gpu")
        self.driver = webdriver.Chrome(options=options)
        self.base_url = "https://dak.gg/er/players/"
        self.player_name = player_name
        self.season = "/matches?season=SEASON_" + str(season) + "&gameMode=RANK&page="
        self.page_num = 1
        self.datas = {
            "RANK": [],
            "MMR": [],
            "TK": [],
        }

        self.player_name = player_name

    def crawling_mmr_change(self):
        crawling_url = self.base_url + self.player_name + self.season
        while True:
            self.driver.get(url=crawling_url + str(self.page_num))
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located(
                        (
                            By.XPATH,
                            '//*[@id="content-container"]/div[2]/section[2]/div[1]',
                        )
                    )
                )
                exchange_options = self.driver.find_element(
                    By.XPATH, '//*[@id="content-container"]/div[2]/section[2]/div[1]'
                ).text
                data_list = exchange_options.split()
                for i, index in enumerate(data_list):
                    if index == "랭크":
                        self.datas["RANK"].append(data_list[i - 1])
                        self.datas["MMR"].append(int(data_list[i + 19]))
                        self.datas["TK"].append(int(data_list[i + 7]))
                if len(data_list) == 4:
                    break
                self.page_num += 1
            except Exception as e:
                break
        for i in self.datas.values():
            i.reverse()
        self.driver.quit()

    def save(self):
        db_dir = os.environ.get("DB_DIR", "./datas")
        Json().save(f"{db_dir}/user/{self.player_name}.json", self.datas)
