# This is the MLB-StatsAPI that i'm using, you can check up it's documentation at
# https://github.com/toddrob99/MLB-StatsAPI/wiki
import statsapi
from datetime import datetime
import requests

def main():
    # url = "https://statsapi.mlb.com/api/v1/gameStatus"
    # print(statsapi.boxscore_data(778414, timecode=None))
    print(statsapi.boxscore(565997,battingInfo=False,fieldingInfo=False,pitchingBox=False,gameInfo=False))
    return None

def getToday():
    today = datetime.utcnow().strftime('%Y-%m-%d')
    print(today)
    return today


# This function returns the gameID which would be needed when we want to call on other stuff
# example of return: 778414
def getGameID():
    games = statsapi.schedule(team=135)
    for x in games:
        id = x['game_id']
        print(id)
    return id

# Returns the current score, home, then away.
def getCurrentScore():
    games = statsapi.schedule(team=135)
    for x in games:
        home_score = x['home_score']
        away_score = x['away_score']
    print(home_score, away_score)
    return home_score, away_score

def getInning():
    games = statsapi.schedule(team=135)
    for x in games:
        inning_state = x['inning_state']
        current_inning = x['current_inning']
    print(inning_state, current_inning)
    return inning_state, current_inning

# Returns the status of the game
# I think it reutnrs the "detailedState" from this url: https://statsapi.mlb.com/api/v1/gameStatus
def getStatus():
    games = statsapi.schedule(team=135)
    for x in games:
        status = x['status']
    print(status)
    return status

if __name__ == '__main__':
    main()