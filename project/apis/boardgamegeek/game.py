import json
import csv
from time import sleep
import requests
import traceback
from bs4 import BeautifulSoup

BASE_URL = "https://boardgamegeek.com/xmlapi"

def user_games(username): 
    game_ids = []
    try: 
        url = f"https://boardgamegeek.com/collection/user/{username}?own=1&subtype=boardgame&ff=1"
        r = requests.get(url)
        result =  r.text
        soup = BeautifulSoup(result, features="lxml") 
        # all td's with a specific class
        tds = soup.find_all("td", class_="collection_objectname")
        for td in tds:
            # href attribute of all a tags in this td tag
            href = td.a["href"] 
            parts = href.split("/")
            game_id = parts[2] 
            game_ids.append(game_id)
        return game_ids
    except Exception as e:
        print(traceback.format_exc()) 

def parse_game(game_id):
    game = {}
    try: 
        print(f"Sending request for {game_id}")
        url = f"{BASE_URL}/boardgame/{game_id}"
        r = requests.get(url)
        result =  r.text
        soup = BeautifulSoup(result, features="lxml")
        game_tag = soup.boardgame
        game["name"] = game_tag.find(primary="true").string
        game["other_names"] = []
        for name_tag in game_tag.find_all("name"): 
            if name_tag.primary == "true":
                game["name"] = name_tag.string 
            else:
                game["other_names"].append(name_tag.string )
        game["year"] = int(game_tag.yearpublished.string)
        game["min_players"] = game_tag.minplayers.string
        game["max_players"] = game_tag.maxplayers.string
        game["min_playtime"] = game_tag.minplaytime.string
        game["max_playtime"] = game_tag.maxplaytime.string
        game["description"] = game_tag.description.string
        game["awards"] = []
        for award in game_tag.find_all("boardgamehonor"):
            game["awards"].append(award.string)
        print(f"{game_id} parsed")
        return game
    except Exception as e:
        print(traceback.format_exc())

game_ids = user_games("Piata")
games = []
for i, game_id in enumerate(game_ids):
    game = parse_game(game_id) 
    games.append(game)
    sleep(0.5)
    if i == 10:
        break
    
# let's write data as json
with open("games.json", "w") as outfile:
    outfile.write(json.dumps(games, indent=4))

# let's write as csv 
fields = ['name', 'other_names', 'year', 'min_players', "max_players", 'max_playtime', 'description', 'awards', 'min_playtime']
# writing to csv file
with open("games.csv", 'w', newline='', encoding="utf8") as csvfile:
    # creating a csv dict writer object
    writer = csv.DictWriter(csvfile, fieldnames=fields)
    # writing headers (field names)
    writer.writeheader()
    # writing data rows
    writer.writerows(games)

# example of downloading an image
# if you are going to build an HTML page with data, there is no need to download
# just store the URL of the image and use that to display the image
url = "https://cf.geekdo-images.com/8UajaMECbrYyJFnXbnpXJQ__listitem/img/0nJ4wREhTIBOZB1Y0T61hjzhDF4=/fit-in/175x175/filters:strip_icc()/pic7591952.png"
r = requests.get(url) 
# open mode 'wb' means *w*rite as *b*inary
with open("image.png", 'wb') as imgfile:
    # r.content is a byte string of response's content (ie excluding headers)
    imgfile.write(r.content)

    

