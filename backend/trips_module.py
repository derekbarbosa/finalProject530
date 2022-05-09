'''
trips module - users can save trips to mogoDB and access them later
uses google api for directions, trip distance, hotel search, total cost
uses EIA api to get current cost of petroleum gasoline
'''

import googlemaps
import requests
import math
from pymongo import MongoClient
from dotenv import load_dotenv
from datetime import datetime
import os

load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY")
gmaps = googlemaps.Client(key=API_KEY)

DB_PASS = os.environ.get("MONGO_DB_PASS")
GAS_KEY = os.environ.get("EIA_API_KEY")


def add_trip(username, destination, departure_date, return_date, airline,
             hotel):
    client = MongoClient(
        f"mongodb+srv://ec530TTY:{DB_PASS}@cluster0.ds0t5.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
    )
    db = client["TTY"]
    trips_collection = db["Trips"]
    if trips_collection.find_one({
            "username": username,
            "destination": destination,
            "departure_date": departure_date
    }):
        return 0
    else:
        trips_collection.insert_one({
            "username": username,
            "destination": destination,
            "departure_date": departure_date,
            "return_date": return_date,
            "airline": airline,
            "hotel": hotel
        })
        return 1


def get_trip(username, destination, departure_date):
    client = MongoClient(
        f"mongodb+srv://ec530TTY:{DB_PASS}@cluster0.ds0t5.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
    )
    trips_collection = client.get_collection("Trips")
    trip = trips_collection.find_one({
        "usernmae": username,
        "destination": destination,
        "departure_date": departure_date
    })
    if trip:
        return trip
    else:
        return 0


#Gas Price of the Month --> added below to get_gas_cost()
# gas_api_param={'api_key':GAS_KEY, 'series_id': 'TOTAL.RUUCUUS.M'}
# gas_api = requests.get('https://api.eia.gov/series/?', gas_api_param)
# gas_price = gas_api[1][7][1]


#retrieve lat,long from gmaps api
def get_geocode(destination):
    return gmaps.geocode(destination)


def reverse_geocode(coordinates):
    return gmaps.reverse_geocode(coordinates)


#return num_hotels hotels from a google maps hotels query at destination; uses geocode to get lat,long tuple from desination
def find_hotels(destination, num_hotels):
    g_code = get_geocode(destination)

    latitude = g_code[0]['geometry']['bounds']['northeast']['lat']
    longitude = g_code[0]['geometry']['bounds']['northeast']['lng']
    coordinates = (latitude, longitude)

    hotels_list = gmaps.places_nearby(
        location=coordinates,
        keyword="hotels",
        language="en-US",
        open_now=True,
        rank_by="distance",
        type="lodging",
    )

    custom_list = {}
    results_list = []

    for i in range(0, int(len(hotels_list))):
        name = hotels_list['results'][i]['name']
        results_list.append("vicinity: " +
                            str(hotels_list['results'][i]['vicinity']))
        results_list.append("Rating: " +
                            str(hotels_list['results'][i]['rating']))
        custom_list[name] = results_list

    return custom_list


#returns driving directions, origin destination should be in strings --> ouput is JSON format
def get_directions(origin, destination):
    if isinstance(origin, str) and isinstance(destination, str):
        route = gmaps.directions(origin, destination)

        trip_distance = route[0]['legs'][0]['distance']['text']
        trip_distance = "".join(filter(str.isdigit, trip_distance))
        trip_distance = int(trip_distance)

        trip_duration = route[0]['legs'][0]['duration']['text']

        steps = route[0]['legs'][0]['steps']
        i = 0
        directions = []
        while i < len(steps):
            directions.append(f"step {i}: " + steps[i]['html_instructions'])
            i += 1

        return trip_distance, trip_duration, directions

    else:
        return 0, 0, 0


#returns gas cost for trip based on inputed distance, tank size and mpg
def get_gas_cost(origin, destination, tank_size, mpg):
    mpg = int(mpg)
    tank_size = int(tank_size)
    gas_api_param = {'api_key': GAS_KEY, 'series_id': 'TOTAL.RUUCUUS.M'}
    gas_api = requests.get('https://api.eia.gov/series/?', gas_api_param)
    gas_api_response = gas_api.json()
    gas_price = gas_api_response['series'][0]['data'][0][1]

    trip_distance, trip_duration, directions = get_directions(
        origin, destination)

    if (trip_distance == 0):
        return -1
    else:
        gallons_needed = math.ceil(trip_distance / mpg)

        if (gallons_needed / tank_size < 1):
            refills_needed = 0
        else:
            refills_needed = math.ceil(gallons_needed / tank_size)

        cost = refills_needed * (tank_size * gas_price)

        return cost
