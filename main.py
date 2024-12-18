import requests
from dotenv import load_dotenv
import os
import itertools
import time

load_dotenv()
API_KEY = os.getenv("API_KEY")
BASE_URL = "https://asia.api.riotgames.com"

game_match_urls= {
    "tft" : "tft/match/v1/matches/by-puuid",
    "lol" : "lol/match/v5/matches/by-puuid"
}

start = 0
increase= 100
stop = False

def get_puuid(player_tag):
    game_name, tag_line = player_tag.split('#')
    url = f"{BASE_URL}/riot/account/v1/accounts/by-riot-id/{game_name}/{tag_line}"
    headers = {"X-Riot-Token": API_KEY}
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()["puuid"]
    else:
        print("Error:", response.status_code, response.json())
        raise ValueError(f"puuid 가져오기 에러 {response.json()}")
    
def get_match_list(puuid, start=0, count=increase, game="lol"):
    url = f"{BASE_URL}/{game_match_urls[game]}/{puuid}/ids?start={start}&count={count}"
    headers = {"X-Riot-Token": API_KEY}
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        print("Error:", response.status_code, response.json())
        raise ValueError(f"매치 기록 불러오기 실패 {response.json()}")

def get_match_info(match_id):
    url = f"/lol/match/v5/matches/{match_id}"
    headers = {"X-Riot-Token": API_KEY}
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json() #데이터 가공하기
    else:
        print("Error:", response.status_code, response.json())
        raise ValueError(f"puuid 가져오기 {response.json()}")
    
print("Player name+tag example) summoner1#KR1")
player1_name = input("Input Player1 name+tag : ")
player2_name = input("Input Player2 name+tag : ")
player1_puuid = get_puuid(player1_name)
player2_puuid = get_puuid(player2_name)
player1_matches = []
player2_matches = []

while True:
    try:
        print(f"Searching {start}~{start+increase}")
        player1_matches.append(get_match_list(player1_puuid,start))
        player1_matches_flat = list(itertools.chain(*player1_matches))
        player2_matches.append(get_match_list(player2_puuid,start))
        player2_matches_flat = list(itertools.chain(*player2_matches))
    except ValueError as e:
        print(f"통신 오류 {e}")

    common_values = list(set(player1_matches_flat) & set(player2_matches_flat))
    if stop:
        print(f"Found {len(common_values)} common matches in {start+increase} matches")
        print(common_values)
        break
    if common_values:
        print(f"Common matches found")
        stop = True
        start+=increase
    else:
        start+=increase
    time.sleep(3) #Control API rate imit