'''
trips module - users can save trips to mogoDB and access them later
uses google api to 
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

#Gas Price of the Month
gas_api_param={'api_key':GAS_KEY, 'series_id': 'TOTAL.RUUCUUS.M'}
gas_api = requests.get('https://api.eia.gov/series/?', gas_api_param)
gas_price = gas_api[1][7][1]


#retrieve lat,long from gmaps api
def get_geocode(destination):
    return gmaps.geocode(destination)

def reverse_geocode(coordinates):
    return gmaps.reverse_geocode(coordinates)

#return an address, enter coordinates+radius, return multiple hotels --> output is JSON format
def find_hotels(coordinates, distance):
    hotel_list = gmaps.places_nearby(
        location=coordinates,
        keyword="hotels",
        language="en-US",
        open_now=True,
        rank_by="distance",
        type="lodging",
        radius=distance
    )
    return hotel_list

# #returns singular hotel based on coordinates/
# def get_hotel(coordinates):
#     hotel = gmaps.find_place(
#         "hotels",
#         "textquery",
#         fields=["formatted_address", "name", "geometry"],
#         location_bias=coordinates,
#         language="en-US"
#     )
#     return hotel

#returns driving directions, origin destination should be in strings --> ouput is JSON format
def get_directions(origin,destination):
    route = gmaps.directions(origin, destination)
    return route

def get_mpg(car):
    pass