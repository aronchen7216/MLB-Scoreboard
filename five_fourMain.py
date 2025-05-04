import statsapi
from urllib.request import urlopen as uReq
import json
import time
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from datetime import datetime
import sys
import random

import backend


# Default Values
DEFAULT_TEAM = 135
DEFAULT_CITY = "San Diego, California"
SERVER_CITY = "Boston, Massachusetts"

# Prompts the user to choose their team
while True:
    s = input(f"Please enter a team ID: ")
    try:
        DEFAULT_TEAM = int(s)
        break
    except ValueError:
        print("Not a valid number, try again")

# Process City Argument. Default is San Diego. In quotes, put in city folowed by a comma then state or country.
# Examples argument: "San Diego, California". "Berlin, Germany"
if len(sys.argv) == 2:
    DEFAULT_CITY = sys.argv[1]
elif len(sys.argv) == 1:
    pass
else:
    print("Please provide at most one city name")
    exit(1)

# For Latency, process distance from server in Boston
distCalc = Nominatim(user_agent="distance_calculator")
host = distCalc.geocode(DEFAULT_CITY)
server = distCalc.geocode(SERVER_CITY)

coordHost = (host.latitude, host.longitude)
coordServer = (server.latitude, server.longitude)
distance = geodesic(coordHost, coordServer).miles

mean = ((51 ** (1 / 11620)) ** distance) / 5
std = ((51 ** (1 / 11620)) ** distance) / 20

if __name__ == "__main__":
    backend.getData(DEFAULT_CITY, mean, std, DEFAULT_TEAM)
