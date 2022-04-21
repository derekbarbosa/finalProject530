from flask import Flask
from flask_restful import Resource, Api
from . import user_module as user

app = Flask(__name__)
api = Api(app, catch_all_404s=True)

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


api.add_resource(Home, "/")
api.add_resource(AddUser, "/user-module/add-user/<string:username>/<string:password>/<string:recovery_email>")
api.add_resource(AuthenticateUser, "/user-module/authenticate-user/<string:username>/<string:password>")

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port=80, debug=True)