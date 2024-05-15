import csv 
import json
import os
from pathlib import Path 
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.mount("/static", StaticFiles(directory="./static"), name="static")

def convert_csv():
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

@app.get("/my_charts")
async def my_charts():
    with open("chart1.html", 'r', newline='', encoding="utf8") as inpfile:
        content = inpfile.read()
    return HTMLResponse(content)

