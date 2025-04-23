import requests

url = "https://statsapi.mlb.com/api/v1.1/game/778414/feed/live"
response = requests.get(url)
data = response.json()

# Get home and away team names
home_team = data["gameData"]["teams"]["home"]["name"]
away_team = data["gameData"]["teams"]["away"]["name"]
print("Home:", home_team, "| Away:", away_team)

# Get inning and half
inning = data["liveData"]["linescore"]["currentInning"]
half = data["liveData"]["linescore"]["inningHalf"]
print(f"{half} of inning {inning}")

# Get current scores for both teams
home_score = data["liveData"]["linescore"]["teams"]["home"]["runs"]
away_score = data["liveData"]["linescore"]["teams"]["away"]["runs"]
print(f"{away_team}: {away_score}")
print(f"{home_team}: {home_score}")

# Get occupied bases
runners = data["liveData"]["plays"]["currentPlay"]["runners"]

# Track base occupancy
bases = {
    1: False,
    2: False,
    3: False
}

# Loop through all runners on base
for runner in runners:
    if "movement" in runner and runner["movement"]["end"] is not None:
        base_str = runner["movement"]["end"]
        if base_str == "1B":
            bases[1] = True
        elif base_str == "2B":
            bases[2] = True
        elif base_str == "3B":
            bases[3] = True

# Print which bases are occupied
for base, occupied in bases.items():
    if occupied:
        print(f"Runner on {base}B")
if not any(bases.values()):
    print("Bases are empty")