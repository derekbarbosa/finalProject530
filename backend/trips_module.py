'''
trips module - users can save trips to mogoDB and access them later
'''

from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

DB_PASS = os.environ.get("MONGO_DB_PASS")

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

