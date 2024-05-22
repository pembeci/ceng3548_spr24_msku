import csv 
import json
import os
from pathlib import Path 
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.mount("/static", StaticFiles(directory="./static"), name="static")

def convert_csv_bos_1980():
    BASE_PATH = os.path.dirname(os.path.abspath(__file__))
    fname = Path(BASE_PATH, "..", "datasets", "nba_data.csv")
    with open(fname, 'r', newline='', encoding="utf8") as inpfile:
        reader = csv.DictReader(inpfile)
        rows = []
        for row in reader:
            if row['Year'] != '1980' or row['Tm'] != 'BOS':
                continue
            rows.append(row)
            print(row)
    with open("bos_1980.json", 'w', newline='', encoding="utf8") as outfile:
        json.dump(rows, outfile)

def convert_csv_all_data():
    BASE_PATH = os.path.dirname(os.path.abspath(__file__))
    fname = Path(BASE_PATH, "..", "datasets", "nba_data.csv")
    data = {}
    with open(fname, 'r', newline='', encoding="utf8") as inpfile:
        reader = csv.DictReader(inpfile)
        rows = []
        for row in reader:
            team = row.pop('Tm')
            if team not in data:
                data[team] = {}
            year = row.pop('Year')
            if year not in data[team]:
                data[team][year] = []
            data[team][year].append(row)
    return data 

nba_data = convert_csv_all_data()
print(nba_data['TOR']['2007'][:3])

@app.get("/my_charts")
async def my_charts():
    with open("chart1.html", 'r', newline='', encoding="utf8") as inpfile:
        content = inpfile.read()
    return HTMLResponse(content)

@app.get("/team_data/{team_name}/{season}")
async def team_data(team_name, season):
    data = nba_data[team_name][season]
    return data

@app.get("/physical_data/")
async def physical_data():
    data = []
    players_found = set()
    for team, year_dict in nba_data.items():
        for year, rows in year_dict.items():
            for row in rows:
                player = row['Player'] 
                if player in players_found:
                    continue
                players_found.add(player)
                weight = row['Weight']
                height = row['Height']
                if weight == '' or height == '':
                    continue
                data.append({
                    "player": player, 
                    "x": float(height),
                    "y": float(weight)
                })
    return data
