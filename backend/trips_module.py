'''
trips module - users can save trips to mogoDB and access them later
'''

import googlemaps
import requests
from pymongo import MongoClient
from dotenv import load_dotenv
from datetime import datetime
import os

load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY")
gmaps = googlemaps.Client(key=API_KEY)

DB_PASS = os.environ.get("MONGO_DB_PASS")
GAS_KEY = os.environ.get("EIA_API_KEY")

def add_trip(username, destination, departure_date, return_date, airline, hotel):
    client = MongoClient(f"mongodb+srv://ec530TTY:{DB_PASS}@cluster0.ds0t5.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
    db = client["TTY"]
    trips_collection = db["Trips"]
    if trips_collection.find_one({"username":username, "destination":destination, "departure_date":departure_date}):
        return 0
    else:
        trips_collection.insert_one({"username":username, "destination":destination, "departure_date":departure_date,"return_date":return_date, "airline":airline, "hotel":hotel})
        return 1

def get_trip(username, destination, departure_date):
    client = MongoClient(f"mongodb+srv://ec530TTY:{DB_PASS}@cluster0.ds0t5.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
    trips_collection = client.get_collection("Trips")
    trip = trips_collection.find_one({"usernmae":username, "destination":destination, "departure_date":departure_date})
    if trip:
        return trip
    else:
        return 0


#coordinates == lat,longitude
#destination == address
gas_api_param={'api_key':GAS_KEY, 'series_id': 'TOTAL.RUUCUUS.M'}
gas_api = requests.get('https://api.eia.gov/series/?', gas_api_param)
gas_price = gas_api[1][7][1]


#retrieve lat,long from gmaps api
def get_geocode(destination):
    geocode = gmaps.geocode(destination)
    latitude = geocode[0]['geometry']['bounds']['northeast']['lat']
    longitude = geocode[0]['geometry']['bounds']['northeast']['lng']
    return latitude,longitude

#still in progress
def reverse_geocode(coordinates):
    return gmaps.reverse_geocode(coordinates)

#return an address, enter coordinates+radius, return multiple hotels
def find_hotels(destination):
    lat, long = get_geocode(destination)
    hotel_data = gmaps.places_nearby(
        location=(lat,long),
        keyword="hotels",
        language="en-US",
        open_now=True,
        rank_by="distance",
        type="lodging",
    )
    return hotel_data['results']

#returns singular hotel based on coordinates -- NEED TO FIX
def get_hotel(lat, long):
    hotel = gmaps.find_place(
        "hotels",
        "textquery",
        fields=["formatted_address", "name", "geometry"],
        location_bias=(lat, long),
        language="en-US"
    )
    return hotel

#returns driving directions, origin destination should be in strings
def get_directions(origin,destination):
    route = gmaps.directions(origin, destination)
    return route

def get_mpg(car):
    pass