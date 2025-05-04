from flask import Flask, jsonify, render_template
import statsapi
from urllib.request import urlopen as uReq
import json
import time

app = Flask(__name__)

TEAM_ID = 108

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data')
def get_game_data():
    today = time.strftime('%Y-%m-%d')
    game = statsapi.schedule(team=TEAM_ID)

    if not game:
        game_id = statsapi.last_game(TEAM_ID)
    else:
        game_id = game[0]['game_id']



    url = f"https://statsapi.mlb.com/api/v1.1/game/{game_id}/feed/live"

    try:
        uClient = uReq(url)
        byteFile = uClient.read()
        uClient.close()
        jsonFile = json.loads(byteFile)

        inning = jsonFile["liveData"]["linescore"]["currentInning"]
        half = jsonFile["liveData"]["linescore"]["inningHalf"]
        outs = jsonFile["liveData"]["plays"]["currentPlay"]["count"]["outs"]

        if outs == 3:
            if half == "Top":
                half = "Middle"
            else:
                half = "End"

        home_score = jsonFile["liveData"]["linescore"]["teams"]["home"]["runs"]
        away_score = jsonFile["liveData"]["linescore"]["teams"]["away"]["runs"]
        home_team = jsonFile["gameData"]["teams"]["home"]["name"]
        away_team = jsonFile["gameData"]["teams"]["away"]["name"]
        # Print the team abbreviation
        homeAbbr = jsonFile['gameData']['teams']['home']['abbreviation']
        awayAbbr = jsonFile["gameData"]["teams"]["away"]["abbreviation"]

        pitcher = jsonFile["liveData"]["plays"]["currentPlay"]["matchup"]["pitcher"]["fullName"]
        batter = jsonFile["liveData"]["plays"]["currentPlay"]["matchup"]["batter"]["fullName"]

        onDeck = jsonFile["liveData"]["linescore"]["offense"]["onDeck"]["fullName"]
        inHole = jsonFile["liveData"]["linescore"]["offense"]["inHole"]["fullName"]

        info = jsonFile["liveData"]["boxscore"].get("info", [])
        pitcherLastName = pitcher.split(" ")[-1]
        pitch_count = "?"

        for i in range(len(info)):
            if info[i]["label"] == "Pitches-strikes":
                splitValue = info[i]["value"].split(" ")
                for j in range(len(splitValue)):
                    if pitcherLastName == splitValue[j]:
                        pitch_count = splitValue[j + 1].split("-")[0]
                    elif pitcherLastName + "," == splitValue[j]:
                        pitch_count = splitValue[j + 2].split("-")[0]

        count = jsonFile["liveData"]["plays"]["currentPlay"]["count"]
        base_keys = jsonFile["liveData"]["linescore"]["offense"].keys()
        bases = [int("first" in base_keys), int("second" in base_keys), int("third" in base_keys)]

        return jsonify({
            "pitcher": pitcher,
            "pitchCount": pitch_count,
            "batter": batter,
            "battingStats": "",  # Placeholder if needed
            "awayScore": away_score,
            "homeScore": home_score,
            "awayTeam": away_team,
            "homeTeam": home_team,
            "inningNumber": inning,
            "half": half,
            "balls": count["balls"],
            "strikes": count["strikes"],
            "outs": count["outs"],
            "bases": bases,
            "homeAbbr":homeAbbr,
            "awayAbbr":awayAbbr,
            "onDeck": onDeck,
            "inHole": inHole
        })

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)