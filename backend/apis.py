import googlemaps
import os
from flask import Flask
from flask_restful import Resource, Api
from datetime import datetime

from . import user_module as user
from . import trips_module as trips

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
    def post(self, username, destination, departure_date, return_date, airline, hotel):
        if trips.add_trip(username, destination, departure_date, return_date, airline, hotel):
            return f"Trip to {destination} successfully added"
        else:
            return f"Trip to {destination} already exists"

class GetTrip(Resource):
    def get(self, username, destination, departure_date):
        return trips.get_trip(self, username, destination, departure_date)
        

api.add_resource(Home, "/")
api.add_resource(AddUser, "/user-module/add-user/<string:username>/<string:password>/<string:recovery_email>")
api.add_resource(AuthenticateUser, "/user-module/authenticate-user/<string:username>/<string:password>")
api.add_resource(AddTrip, "/trips-module/add-trip/<string:username>/<string:destination>/<string:departure_date>/<string:return_date>/<string:airline>/<string:hotel>")
api.add_resource(GetTrip, "/trips-module/get-trip/<string:username>/<string:destination>/<string:departure_date>")

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port=80, debug=True)