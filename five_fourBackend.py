import statsapi
from urllib.request import urlopen as uReq
import json
import time
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from datetime import datetime
import random

def getData(city, mean, std, DEFAULT_TEAM):
    # 135 = Padres. 
    # Link for IDs: https://github.com/jasonlttl/gameday-api-docs/blob/master/team-information.md?utm_source=chatgpt.com
    # Get game today.
    while(True):

        # Proceed with data extraction
        game = statsapi.schedule(team=DEFAULT_TEAM) # <- switch ID here if you want to get a different game
        
        # Sleep for an hour if there is no game
        if not game:
            print("No games today!")
            time.sleep(3600)
            continue
        
        else:       
            for a in game:
                game_id = a['game_id'] # Print out the game id to get the live feed.

            # URL to request the live feed.
            url = "https://statsapi.mlb.com/api/v1.1/game/" + F"{game_id}" + "/feed/live"

            totalDelay = 0
            totalIterations = 0

            while(True):

                # Get start time then sleep
                totalIterations += 1
                start = datetime.now()
                time.sleep(random.gauss(mean, std))

                uClient = uReq(url)  # Open up connection
                byteFile = uClient.read()  # Grab the page
                uClient.close()  # We are done with this (for now)

                jsonFile = json.loads(byteFile) # Load file as JSON

                # Probably the structure of a scorecard

                # 1) Inning and half. Shamelessly copied from you.
                inning = jsonFile["liveData"]["linescore"]["currentInning"]
                half = jsonFile["liveData"]["linescore"]["inningHalf"]
                outs = jsonFile["liveData"]["plays"]["currentPlay"]["count"]["outs"]

                # Need to check if there are three outs.
                if outs == 3:
                    if half == "Top":
                        half = "Middle"
                    else:
                        half = "End"

                print("Inning:", half, inning)

                # 2) Scores and teams. Also shamelessly copied from you.
                home_score = jsonFile["liveData"]["linescore"]["teams"]["home"]["runs"]
                away_score = jsonFile["liveData"]["linescore"]["teams"]["away"]["runs"]
                home_team = jsonFile["gameData"]["teams"]["home"]["name"]
                away_team = jsonFile["gameData"]["teams"]["away"]["name"]
                # Print the team abbreviation
                homeAbbr = jsonFile['gameData']['teams']['home']['abbreviation']
                awayAbbr = jsonFile["gameData"]["teams"]["away"]["abbreviation"]

                print("Away team:", away_team)
                print("Away abbreviation:", awayAbbr) 
                print("Home team:", home_team)
                print("Home abbreviation:", homeAbbr)
                print("Score:", away_score, "-", home_score)

                # 3) Pitcher/Pitch Count and Batter Name.
                pitcher = jsonFile["liveData"]["plays"]["currentPlay"]["matchup"]["pitcher"]["fullName"]
                pitcherLastName = pitcher.split(" ")[1]
                batter = jsonFile["liveData"]["plays"]["currentPlay"]["matchup"]["batter"]["fullName"]

                info = jsonFile["liveData"]["boxscore"]["info"]
                infoLength = len(jsonFile["liveData"]["boxscore"]["info"])

                for i in range(infoLength):
                    if(info[i]["label"] == "Pitches-strikes"):
                        splitValue = info[i]["value"].split(" ")
                        for j in range(len(splitValue)):
                            if pitcherLastName == splitValue[j]:
                                splitNumbers = splitValue[j + 1].split("-")[0]
                            elif pitcherLastName + "," == splitValue[j]:
                                splitNumbers = splitValue[j + 2].split("-")[0]

                print("Pitcher:", pitcher)
                print("Pitch Count:", splitNumbers)
                print("Batter:", batter)

                # 4) On deck and in the hole
                onDeck = jsonFile["liveData"]["linescore"]["offense"]["onDeck"]["fullName"]
                inHole = jsonFile["liveData"]["linescore"]["offense"]["inHole"]["fullName"]

                print("On-Deck:", onDeck)
                print("In-the-Hole:", inHole)

                # 5) Count and outs. 

                # To print all counts. 
                '''
                allPlays = jsonFile["liveData"]["plays"]["allPlays"]
                count_allPlays = len(allPlays)

                for i in range(count_allPlays):
                    # Get the ith play of the game
                    ithPlay = allPlays[i]["playEvents"]
                    # There are many updates to the counts like 0-0 to 1-0 or 0-1. We can be stuck at 3-2 with continuous foul balls.
                    count_ithPlay = len(ithPlay)
                    for j in range(count_ithPlay):
                        jthCount_ithPlay = ithPlay[j]["count"]
                        print(jthCount_ithPlay)
                '''

                # To get the current count and outs.
                current_count = jsonFile["liveData"]["plays"]["currentPlay"]["count"]
                print("Count:", current_count["balls"], "-", current_count["strikes"])
                print("Outs:", current_count["outs"])

                '''
                # Get the latest result of an at-bat. This may not always work.
                try:
                    result = jsonFile["liveData"]["plays"]["allPlays"][-1]["result"]["description"]
                    print(result)
                except:
                    pass
                '''

                # Get occupied bases
                runners = jsonFile["liveData"]["plays"]["currentPlay"]["runners"]

                # Track base occupancy
                bases = [0, 0, 0]

                base_keys = jsonFile["liveData"]["linescore"]["offense"].keys()

                if "first" in base_keys:
                    bases[0] = 1
                if "second" in base_keys:
                    bases[1] = 1
                if "third" in base_keys:
                    bases[2] = 1

                # Print which bases are occupied
                print("Bases:", bases)
                
                print() 
                
                # Get the latency statistics
                end = datetime.now()
                diff = end - start
                secs = diff.seconds * 1000
                micros = diff.microseconds / 1000
                total = secs + micros

                totalDelay += total

                print(F"Delay from {city} at this iteration:", "{:.2f}".format(total), "ms")
                print(F"Average delay:", "{:.2f}".format(totalDelay / totalIterations), "ms")

                print() 

                # Make the output look good.
                time.sleep(2)        
