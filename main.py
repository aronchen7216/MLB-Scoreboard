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

# Process City Argument. Default is San Diego. In quotes, put in city folowed by a comma then state or country.
# Examples argument: "San Diego, California". "Berlin, Germany"
if len(sys.argv) == 2:
    city = sys.argv[1]
elif len(sys.argv) == 1:
    city = "San Diego, California"
else:
    print("Please provide at most one city name")
    exit(1)

# For Latency, process distance from server in Boston
distCalc = Nominatim(user_agent="distance_calculator")
host = distCalc.geocode(city)
server = distCalc.geocode("Boston, Massachusetts")

coordHost = (host.latitude, host.longitude)
coordServer = (server.latitude, server.longitude)
distance = geodesic(coordHost, coordServer).miles

mean = distance / 1000
std = mean / 4

if __name__ == "__main__":
    backend.getData(city, mean, std)
