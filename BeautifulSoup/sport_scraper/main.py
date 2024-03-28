import requests
from bs4 import BeautifulSoup
import pandas as pd
import csv


footbol_player = "Daniel Jones"
url = "https://www.pro-football-reference.com/players/K/KazeDa00"
seasonYear = ["/gamelog/2023/", "/gamelog/2022/", "/gamelog/2021/"]

file_name = footbol_player.replace(" ", "-")
f = open(file=file_name, mode="w", newline="")
scrapedGames = csv.writer(f)

for season in seasonYear:

    data = requests.get(url + season).text

    soup = BeautifulSoup(data, "lxml")

    season_table = soup.find("table", id="stats")
    
    statList = []
    header_count = 0
    
    header = season_table.find_all("tr")[1]
    # for header in season_table.find_all("th"):
    statList = [val.text for val in header.find_all("th")]
    scrapedGames.writerow(statList)
    gameArray = []
    breakValue = 0
    
    for game in season_table.find_all("tr")[2:]:
        cols = game.find_all("td")
        statList = [footbol_player]
        
        for col in cols:
            if "Upcoming" in col.text:
                breakValue += 1
                break
            
            statList.append(col.text)
            
            if breakValue == 1:
                break
        
        scrapedGames.writerow(statList)
        gameArray.append(statList)