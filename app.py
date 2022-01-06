from flask import Flask, render_template, url_for
import requests
from flask_cors import CORS
from bs4 import BeautifulSoup
import re

app = Flask(__name__)
CORS(app)

ids_to_region = {
    "MT" : "targon", 
    "BC" : "bandlecity",
    "DE" : "demacia",
    "FR" : "freljord",
    "IO" : "ionia",
    "NX" : "noxus",
    "PZ" : "piltoverzaun",
    "BW" : "bilgewater",
    "SI" : "shadowisles",
    "SH" : "shurima"
    }

# Old legends from Bandlecity are written as the other region
special_cards = {
    "02BW046" : "bilgewater", # Fizz
    "01PZ008" : "piltoverzaun", # Teemo
    "01PZ056" : "piltoverzaun", # Heimerdinger
    "03IO002" : "ionia" # Lulu
}

def get_region_by_id(id):
    # Because two regional followers are always BC, we need to google them
    all_regions = []
    print(f"get_region_by_id invoked with: {id}")
    page = requests.get(f"https://www.google.com/search?q={id} region&num=1")
    soup = BeautifulSoup(page.content, "html.parser")
    links = soup.findAll("a")
    for link in links :
        link_href = link.get('href')
        if "url?q=" in link_href and not "webcache" in link_href:
            fixed_link = link.get('href').split("?q=")[1].split("&sa=U")[0]
            if "leagueoflegends.fandom.com" in fixed_link:
                page = requests.get(fixed_link)
                soup = BeautifulSoup(page.content, "html.parser")
                regions = soup.findAll("div", {"class": "pi-data-value pi-font"})[0]
                for r in regions:
                    result = re.search('data-image-name="(.*) LoR Region.png', str(r))
                    try:
                        all_regions.append(result.group(1).lower().replace(" ", ""))
                    except:
                        continue
    if "bandlecity" in all_regions:
        all_regions.remove("bandlecity")
    print("all_regions found: " + str(all_regions))
    try:
        all_regions = all_regions[0]
        return all_regions
    except:
        pass

all_played_regions = []
all_not_played_regions = ["targon", "bandlecity","demacia","freljord","ionia","noxus","piltoverzaun","bilgewater","shadowisles", "shurima"]

@app.route('/')
def hello():
    return render_template('app.html')


@app.route("/get_from_flask_from_riot/")
def get_from_flask_from_riot():
    global all_played_regions
    global all_not_played_regions
    try:
        all_data = requests.get('http://127.0.0.1:21337/positional-rectangles').json()
    except:
        return "Please log into Legends of Runterra"
    if all_data["GameState"] == "InProgress":
        print("In a game!")
        print(all_data["Rectangles"])
        for card in all_data["Rectangles"]:
            two_letters_of_region = ""
            full_name_of_region = ""
            card_id = card['CardCode']
            for key in ids_to_region:
                if key in card_id:
                    two_letters_of_region = key
                    full_name_of_region = ids_to_region[two_letters_of_region]

            if card["TopLeftY"] == 260 or card["TopLeftY"] == 450 or card["TopLeftY"] == 284 and full_name_of_region in all_not_played_regions:
                print(f"You played: {card_id}")
                if two_letters_of_region == "BC" or card['CardCode'] in special_cards:
                    # Bandle City is special - we need to check for duel
                    all_played_regions.append("bandlecity")
                    try:
                        all_not_played_regions.remove("bandlecity")
                    except:
                        continue
                    all_played_regions.append(get_region_by_id(card_id))
                    try:
                        all_not_played_regions.remove(get_region_by_id(card_id))
                    except:
                        continue
                if two_letters_of_region != "BC":
                    # Easy - just add to all all_played_regions and remove from all_not_played_regions
                    all_played_regions.append(full_name_of_region)
                    try:
                        all_not_played_regions.remove(full_name_of_region)
                    except:
                        continue
        all_played_regions = list(dict.fromkeys(all_played_regions))
        if None in all_played_regions:
            all_played_regions.remove(None)
        return {"played" : all_played_regions, "not played" : all_not_played_regions}
    else:
        all_played_regions = []
        all_not_played_regions = ["targon", "bandlecity","demacia","freljord","ionia","noxus","piltoverzaun","bilgewater","shadowisles", "shurima"]
        return "Please enter a game"

if __name__ == '__main__':
    app.secret_key = "as"
    app.run(debug=True)
