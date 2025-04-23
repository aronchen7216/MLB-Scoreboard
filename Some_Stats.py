import statsapi
from urllib.request import urlopen as uReq
import json

# 135 = Padres, 110 = Orioles
game = statsapi.schedule(team=110) # Get game today.

for a in game:
    game_id = a['game_id'] # Print out the game id to get the live feed.

# URL to request the live feed.
url = "https://statsapi.mlb.com/api/v1.1/game/" + F"{game_id}" + "/feed/live"

uClient = uReq(url)  # Open up connection
byteFile = uClient.read()  # Grab the page
uClient.close()  # We are done with this (for now)

jsonFile = json.loads(byteFile) # Load file as JSON

# Probably the structure of a scorecard

# 1) Inning and half. Shamelessly copied from you.

inning = jsonFile["liveData"]["linescore"]["currentInning"]
half = jsonFile["liveData"]["linescore"]["inningHalf"]

print(half, inning)

# 2) Scores and teams. Also shamelessly copied from you.
home_score = jsonFile["liveData"]["linescore"]["teams"]["home"]["runs"]
away_score = jsonFile["liveData"]["linescore"]["teams"]["away"]["runs"]
home_team = jsonFile["gameData"]["teams"]["home"]["name"]
away_team = jsonFile["gameData"]["teams"]["away"]["name"]

print(away_team, ":", away_score)
print(home_team, ":", home_score)


# 2) Pitcher Name.
#pitcher = jsonFile[]

# 3) Count and outs. 

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
current_count = jsonFile["liveData"]["plays"]["allPlays"][-1]["playEvents"][-1]["count"]
print(current_count)

'''
# Get the latest result of an at-bat. This may not always work.
result = jsonFile["liveData"]["plays"]["allPlays"][-1]["result"]["description"]
print(result)
'''

# print(jsonFile)
