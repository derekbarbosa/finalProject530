import os
import googlemaps

from dotenv import load_dotenv
from flask import Flask
from flask_restful import Resource, Api
from datetime import datetime

import user_module as user
import trips_module as trips

app = Flask(__name__)
api = Api(app, catch_all_404s=True)

load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY")
gmaps = googlemaps.Client(key=API_KEY)


class Home(Resource):

    def get(self):
        return "Home page TTY Rest APIs"


class AddUser(Resource):

    def post(self, username, password, recovery_email):
        return user.add_user(username, password, recovery_email)

    def get(self, username, password, recovery_email):
        return user.check_user(username, password, recovery_email)


class AuthenticateUser(Resource):

    def get(self, username, password):
        return user.authenticate_user(username, password)


class AddTrip(Resource):

    def post(self, username, destination, departure_date, return_date, airline,
             hotel):
        if trips.add_trip(username, destination, departure_date, return_date,
                          airline, hotel):
            return f"Trip to {destination} successfully added"
        else:
            return f"Trip to {destination} already exists"


class GetTrip(Resource):

    def get(self, username, destination, departure_date):
        return trips.get_trip(self, username, destination, departure_date)


class GetHotels(Resource):

    def get(self, destination, num_hotels):
        ret_val = trips.find_hotels(destination, num_hotels)
        if ret_val < 0:
            return "Failed get request"
        else:
            return ret_val


class GetDirections(Resource):

    def get(self, origin, destination):
        distance, duration, directions = trips.get_directions(
            origin, destination)
        if distance == 0 and duration == 0 and directions == 0:
            return "Failed get request"
        else:
            return distance, duration, directions


class GetGasCost(Resource):

    def get(self, origin, destination, tank_size, mpg):
        cost_val = trips.get_gas_cost(origin, destination, tank_size, mpg)
        if cost_val < 0:
            return "Failed get request"
        else:
            return cost_val


api.add_resource(Home, "/")
api.add_resource(
    AddUser,
    "/user-module/add-user/<string:username>/<string:password>/<string:recovery_email>"
)
api.add_resource(
    AuthenticateUser,
    "/user-module/authenticate-user/<string:username>/<string:password>")
api.add_resource(
    AddTrip,
    "/trips-module/add-trip/<string:username>/<string:destination>/<string:departure_date>/<string:return_date>/<string:airline>/<string:hotel>"
)
api.add_resource(
    GetTrip,
    "/trips-module/get-trip/<string:username>/<string:destination>/<string:departure_date>"
)
api.add_resource(
    GetHotels,
    "/trips-module/get-hotels/<string:destination>/<int:num_hotels>")
api.add_resource(
    GetDirections,
    "/trips-module/get-directions/<string:origin>/<string:destination>")
api.add_resource(
    GetGasCost,
    "/trips-module/get-gas-cost/<string:origin>/<string:destination>/<int:tank_size>/<int:mpg>"
)

if __name__ == '__main__':
    app.run(host='localhost', port=8080, debug=True)
