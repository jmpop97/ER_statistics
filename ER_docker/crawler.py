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


erc = Crawler()
erc.crawling_top_players()
del erc
print(1)
