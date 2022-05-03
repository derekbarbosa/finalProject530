import googlemaps
import requests
from dotenv import load_dotenv
from flask import Flask
from flask_restful import Resource, Api
from datetime import datetime
import os

load_dotenv()

GAS_KEY = os.environ.get("EIA_API_KEY")

gas_api_param={'api_key':GAS_KEY, 'series_id': 'TOTAL.RUUCUUS.M'}
gas_api = requests.get('https://api.eia.gov/series/?', gas_api_param).json()
print(gas_api['series'][0]['data'][0][1])


API_KEY = os.getenv("GOOGLE_API_KEY")
gmaps = googlemaps.Client(key=API_KEY)

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

print(hotels_list['results'][1:20])

custom_list = {}

for i in range(0,20):
    name = hotels_list['results'][i]['name']
    results_list = []
    results_list.append(hotels_list['results'][i]['vicinity'], hotels_list['results'][i]['photos'][0]['html_attributions'], hotels_list['results'][i]['rating'])
    custom_list[name] = results_list
    print(custom_list)

#print(hotels_data['results'])