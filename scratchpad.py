import googlemaps
import requests
import math
from dotenv import load_dotenv
from flask import Flask
from flask_restful import Resource, Api
from datetime import datetime
import os

load_dotenv()

GAS_KEY = os.environ.get("EIA_API_KEY")
API_KEY = os.getenv("GOOGLE_API_KEY")

#setup of GMAPs client
gmaps = googlemaps.Client(key=API_KEY)

#calling gas API and parsing for price
gas_api_param={'api_key':GAS_KEY, 'series_id': 'TOTAL.RUUCUUS.M'}
gas_api = requests.get('https://api.eia.gov/series/?', gas_api_param).json()
gas_price = gas_api['series'][0]['data'][0][1]

# tank size in gallons
compact_tank_size = 13
sedan_tank_size = 18
suv_tank_size = 25
truck_tank_size = 30

#average mpg by type
compact_mpg = 35
sedan_mpg = 25
suv_mpg = 25
truck_mpg = 17

#retrieve lat,long from gmaps api
def get_geocode(destination):
    return gmaps.geocode(destination)

#return an address, enter coordinates+radius, return multiple hotels
def find_hotels(lat,long):
    hotel_list = gmaps.places_nearby(
        location=(lat,long),
        keyword="hotels",
        language="en-US",
        open_now=True,
        rank_by="distance",
        type="lodging",
    )

    return hotel_list


# def get_hotel(lat, long):
#     hotel = gmaps.find_place(
#         "hotels",
#         "textquery",
#         fields=["formatted_address", "name", "geometry"],
#         location_bias=(lat, long),
#         language="en-US"
#     )
#     return hotel['candidates']

geocode = get_geocode("Boston, MA")
latitude = geocode[0]['geometry']['bounds']['northeast']['lat']
longitude = geocode[0]['geometry']['bounds']['northeast']['lng']

hotels_list = find_hotels(latitude,longitude)

custom_list = {}

for i in range(0,20):
    name = hotels_list['results'][i]['name']
    results_list = []
    results_list.append(hotels_list['results'][i]['vicinity'])
    results_list.append(hotels_list['results'][i]['photos'][0]['html_attributions'])
    results_list.append(hotels_list['results'][i]['rating'])
    custom_list[name] = results_list


def get_directions(origin,destination):
    route = gmaps.directions(origin, destination)
    return route

route = get_directions("Boston", "NYC")

trip_distance = route[0]['legs'][0]['distance']['text']
trip_distance = "".join(filter(str.isdigit,trip_distance))
trip_distance = int(trip_distance)

#CALCULATOR ASSUMES U START WITH FULL TANK
def get_gas_cost(trip_distance, tank_size, mpg):

    gallons_needed = math.ceil(trip_distance/mpg)
    print(gallons_needed)

    if(gallons_needed/tank_size < 1):
        refills_needed = 0
    else:
        refills_needed = math.ceil(gallons_needed/tank_size)

    print(refills_needed)
    cost = refills_needed*(tank_size*gas_price)

    return cost

print(get_gas_cost(trip_distance,compact_tank_size,compact_mpg))
