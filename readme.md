# ER statstics
Eternalreturn game data analyze
<br>  [notion](#notion)
<br> [skill](#used-skills)
<br> [Project setting](#프로젝트-세팅--사용법)
<br> [code structure](#코드-구성)
<br>[To Do](#todo)
<br>[Member Info](#참가자)
# Notion
[notion 주소](https://dent-crocodile-dde.notion.site/ER-project-3db7e6843eab4906b915b37df5c938c1?pvs=4)

# Used skills
### 📋 Languages
<img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=Python&logoColor=white"> <img src="https://img.shields.io/badge/shell_script-%23121011.svg?style=for-the-badge&logo=gnu-bash&logoColor=white">

### 🖥️ ML/DL
<img src="htt
ps://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white"> <img src="https://img.shields.io/badge/numpy-%23013243.svg?style=for-the-badge&logo=numpy&logoColor=white"> <img src="https://img.shields.io/badge/Matplotlib-%23ffffff.svg?style=for-the-badge&logo=Matplotlib&logoColor=black">

### ☁️ Hosting/SaaS
<img src="https://img.shields.io/badge/AWS-%23FF9900.svg?style=for-the-badge&logo=amazon-aws&logoColor=white">

### 💾 Databases
<img src="https://img.shields.io/badge/MongoDB-%234ea94b.svg?style=for-the-badge&logo=mongodb&logoColor=white">

# 프로젝트 세팅 / 사용법 
## 프로젝트 세팅
```
pip install -r requirements
python project.py
```
## 데이터 저장
<br>ER_apis/ER_api.py ERAPI().save_games()에서 게임 데이터 저장
## 프로젝트 사용법1
<br>ER_fig/figure_Datas.py의 객체 실행
## 프로젝트 사용법2
<br>ER_datas/data_class을 통해 필요 데이터 정제
<br>다양한 방법을 통한 시각화 제작

## 테스트 코드 실행
```
python -m unittest
```

# 코드 구성
## ER_EC2
<br>aws ec2 인스턴스를 ER api 저장하는 mongoDB로 설정하는 관련 코드
<br>[Link to manual readme.md](./ER_EC2/readme.md)
## ER_apis
* ER_api.py
<br>공식 api 받는함수
    * ERAPI().save_games(start_game: int,n: int = 1,second: int = 1,game_type: list = ["Rank", "Normal", "Cobalt"],duplication: bool = True,reverse: bool = True,d: int = 1,root_dir: str = "")
<br>게임 데이터 저장
## ER_datas
* ERDataCleansing.py
    * ERDataCleansing(data_class=DataClass(),game_mode=["Rank"],DB_type: str = "",major_version: int = -1,minor_version: int = -1)  
        data_class : 정제된 데이터 
        
* data_class.py  
    * DataClass(conditions) 
        <br>데이터 처리 기본 Class,상속 받아서 ERdataCleansing과 함께 쓸 것
        * add_data(user_data) 
        유저별 데이터 읽은 후 처리
        * add_data_game_id() 
        게임별 데이터 읽은 후 처리
        * last_calculate() 
        모든 데이터 읽은 후 처리
        <br>
    * TestClass(DataClass) 
        <br>ERDataCleansing을 테스트 하기 위한 클래스
        <br><br>
    * DicCharacterFilterData(*condition) 
        <br>캐릭별 condition 데이터
        * dic_characterNum_datas : list = [{condition : data , ...} , ...] 
        <br><br>
    * DicCharacterData(*condition) 
        <br>캐릭별 데이터
        * dic_characterNum_datas["characterNum"][condition] : list = [data , ...] 
        <br><br>
    * ListFilterData(*condition,**name_dic) 
        <br>codition 계산 및 condition 이름 변경
        * conditions[condition] : list [data , ...] 
        <br><br>
    * ForeignTeam(*condition) 
        <br>팀이 같은 나라 사람끼리 매칭 되었는지 확인
        * team[team][condition] : list = [data] 
        team="domestic_team","foreigner_team"
        <br><br>
    * EmoticonMMRClass(*condition)
        <br>이모티콘 소통
        <br><br>
    * CharacterClass(*condition) 
        <br>탱커/딜러/서폿
        <br><br>
    * Camera_All(*condition) 
        <br>카메라별 데이터
        <br><br>
    * Hyperloop(*condition) 
        <br>하이퍼 루프별 데이터
        <br><br>
    * GetMMRFromRankByTier()
        <br>티어별 mmr획득량
        * datas[condition] : list = [data , ...]<br>
        condition = "mmrRank","mmrGainInGame","Tier","gameRank"
        <br><br>
    * GetMMRFromRank(*condition) 
        <br>250단위의 mmr별 데이터
        * datas[condition] : list = [data , ...] 
        condition = "gameRank", "mmrRank", "mmrGainInGame", "mmrBefore_range250"
## ER_docker
* crawler.py
    <br>데이터 크롤링
    * Crawler(param_dict: dict = {"teamMode": "SQUAD", "serverName": "seoul", "season": "11"})
        * crawling_top_players() -> [[name,tier,RP-rank1-rank3-play-mean_rank-kill], ...]
        <br> 랭킹 1000등까지의 유저 목록
        <br><br>
    * DakPlayerCrawler(player_name,season)
        * crawling_mmr_change()
        * get_mmr_change()
        <br> 유저의 mmr 변동량 list
## ER_fig
* figure_datas.py 
    <br>데이터 시각화 하는 범용적인 툴 제작  → seaborn 등 툴을 사용하여 결과를 보는 객체 생성
    * FigureType 
        <br>범용적인 figure 객체로 삭제 예정
        <br><br>
    * FigTierGetMMR 
        <br>티어별 mmr 획득량
        <br><br>
    * FigTierGetMMRFromRank 
        <br>랭크별 mmr 획득량
        <br><br>
    * FigTierGetMMRByRankWithTier 
        <br>티어별 랭킹에서 평균 mmr획득량 
        <br>x : 랭킹 , y : mmr획득량, hue : Tier 
        <br><br>
    * FigTierGetMMRByRankWithBeforeMMR 
        <br>mmr(range250)별 랭킹에서 평균 mmr획득량 
        <br>x : 랭킹 , y : mmr획득량, hue : mmr(range250) 
        <br><br>
    * FigRankPerTier 
        <br>티어별 랭킹 비율 (V13,V15 : 큰 차이가 없음)
        <br><br>
    * FigRankPerMMR 
        <br>mmr 랭킹 비율 (다이아 부터 top3에서 큰차이가 있음)
## public_setting
* variable.py
    * Tier
    <br>게임 버전에 따른 티어 값 대입 필요
        * Tier_names
    <br>티어별 이름 정렬(아이언~데미갓)
        * tier_name(mmr : int) -> str
    <br>mmr값에 따른 티어값
        * tier_cost(n) -> int:
    <br>티어에 따른 입장료값
    <br>n : int = mmr
    <br>n : str = 티어
    * game_DB(types: list = ["Colbalt", "Normal", "Rank"],
major_version: int = [`'*'`],minor_version: int = [`'*'`],root_dir: str = "")
<br>DB설정
        - game_list : list
        <br>DB에 있는 게임 id
        - dir_list : list
        <br>DB의 게임 데이터 

# TODO
1. 깃 버전에 따른 업데이트 함수
2. 게임 버전에 의한 변수 변동(티어입장료, 티어 기준)
3. 테스트 코드에 대한 범용성 & 예시 데이터 제공 문제
4. ERDataCleansing중 진행도 확인 추가(Model-View)
5. 자체적 코드 작성이 아닌 결과만 보고 싶은 사람을 위한 py함수(MVC모델)
6. ERAPI().save_games() - 비교 함수 시간복잡도 최적화
7. 한 유저의 최종 mmr 추측(ODE solution, 시계열 분석, 빈도수를 통한 예측)
8. PR시 description 자동 생성
9. 추가 예정

# 참가자
이름|이메일|깃 주소|블로그|
---|---|---|---|
박종민|pjm970128@gmail.com|https://github.com/jmpop97|https://jmpop.tistory.com/|
유동국|bb06001@naver.com|https://github.com/dbehdrnr0202|---|
안수호|---|---|---|

