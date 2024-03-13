# ER statstics
<br> Eternalreturn game data analyze <br/>
[분석 방법-data_class.py](#mainpy)


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


# Notion
[notion 주소](https://dent-crocodile-dde.notion.site/ER-project-3db7e6843eab4906b915b37df5c938c1?pvs=4)
# 참가자
이름|이메일|깃 주소|블로그|
---|---|---|---|
박종민|pjm970128@gmail.com|https://github.com/jmpop97|https://jmpop.tistory.com/|
유동국|bb06001@naver.com|https://github.com/dbehdrnr0202|---|
안수호|---|---|---|

# projectsetting.py
프로젝트 설치
# main.py
프로젝트 코드
* ER_apis<br/>
    * ER_api.py<br/>
        * - ERAPI().save_games(start_game: int,n: int = 1,second: int = 1,game_type: list = ["Rank", "Normal", "Cobalt"],duplication: bool = True,reverse: bool = True,d: int = 1,root_dir: str = "")<br/>
        * 게임 데이터 저장<br/>
* ER_datas<br/>
    * ERDataCleansing.py<br/>
        * ERDataCleansing(data_class=DataClass(),game_mode=["Rank"],DB_type: str = "",major_version: int = -1,minor_version: int = -1)<br/> 
        DataClass : 정제된 데이터<br/>
    * data_class.py <br/>
        * DataClass(conditions)<br/>
        데이터 처리 기본 Class,상속 받아서 ERdataCleansing과 함께 쓸 것
        * - add_data(user_data)<br/>
        유저별 데이터 읽은 후 처리
        * - add_data_game_id()<br/>
        게임별 데이터 읽은 후 처리
        * - last_calculate()<br/>
        모든 데이터 읽은 후 처리        
        <br/>
        * TestClass(DataClass)<br/>
        ERDataCleansing을 테스트 하기 위한 클래스
        <br/>
        * DicCharacterFilterData(*condition)<br/>
        캐릭별 condition 데이터
        * - dic_characterNum_datas : list = [{condition : data , ...} , ...]<br/>
        <br/>
        * DicCharacterData(*condition)<br/>
        캐릭별 데이터
        * - dic_characterNum_datas["characterNum"][condition] : list = [data , ...]<br/>
        <br/>
        * ListFilterData(*condition,**name_dic)<br/>
        codition 계산 및 condition 이름 변경
        * - conditions[condition] : list [data , ...]<br/>
        <br/>
        * ForeignTeam(*condition)<br/>
            팀이 같은 나라 사람끼리 매칭 되었는지 확인
        * - team[team][condition] : list = [data]<br/>
        team="domestic_team","foreigner_team"
        <br/>
<br/>
        * EmoticonMMRClass(*condition)<br/>
        이모티콘 소통
        <br/>
<br/>
        * CharacterClass(*condition)<br/>
        탱커/딜러/서폿
        <br/>
        * Camera_All(*condition)<br/>
        카메라별 데이터
<br/>
        <br/>
        * Hyperloop(*condition)<br/>
        하이퍼 루프별 데이터
        <br/><br/>
        * GetMMRFromRankByTier()
        <br/> 티어별 mmr획득량
        * - datas[condition]<br>
        condition = "mmrRank","mmrGainInGame","Tier","gameRank"
        <br/><br/>
        * GetMMRFromRank(*condition)<br/>
        250단위의 mmr별 데이터
        * - datas[condition] : list = [data , ...]<br/>
        condition = "gameRank", "mmrRank", "mmrGainInGame", "mmrBefore_range250"

* ER_fig
    * figure_datas.py<br/>
    데이터 시각화 하는 범용적인 툴 제작  → seaborn 등 툴을 사용하여 결과를 보는 객체 생성
        * FigureType<br/>
    범용적인 figure 객체로 삭제 예정
        * FigTierGetMMR<br/>
        티어별 mmr 획득량(V13이하만 적용 가능,시즌 변화에 의한 티어별 mmr 변동 문제)
        * FigTierGetMMRFromRank<br/>
        (V13문제로 리펙토링 필요)
        * FigTierGetMMRByRankWithTier<br/>
        티어별 랭킹에서 평균 mmr획득량<br/>
        x : 랭킹 , y : mmr획득량, hue : Tier<br/>
        * FigTierGetMMRByRankWithBeforeMMR<br/>
        mmr(range250)별 랭킹에서 평균 mmr획득량<br/>
        x : 랭킹 , y : mmr획득량, hue : mmr(range250)<br/>
        * FigRankPerTier<br/>
        티어별 랭킹 비율 (V13,V15 : 큰 차이가 없음)<br>
        * FigRankPerMMR<br/>
        mmr 랭킹 비율 (다이아 부터 top3에서 큰차이가 있음)<br>
* public_setting
    * variable.py
        * Tier<br>
        게임 버전에 따른 티어 값 대입 필요
        * - Tier_names<br>
        티어별 이름 정렬(아이언~데미갓)
        * - tier_name(mmr : int) -> str<br>
        mmr값에 따른 티어값
        * - tier_cost(n) -> int:<br>
        티어에 따른 입장료값<br>
        n : int = mmr<br>
        n : str = 티어<br>
        <br>
        * game_DB(types: list = ["Colbalt", "Normal", "Rank"],
major_version: int = ["*"],minor_version: int = ["*"],root_dir: str = "")<br>
DB설정<br>
        * - game_list : list<br>
        DB에 있는 게임 id
        * - dir_list : list<br>
        DB의 게임 데이터 


# python -m unittest
테스트 코드 실행

# EC2
aws ec2 인스턴스를 ER api 저장하는 mongoDB로 설정하는 관련 코드

[Link to manual readme.md](./ER_EC2/readme.md)

## TODO
.env 설정하기