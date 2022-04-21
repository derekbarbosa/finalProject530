'''
SILL TO DO: REPLACE MONGODB URL IN EACH FUNCTION IN THIS FILE
'''


from pymongo import MongoClient

def check_user(username, password, recovery_email):
    client = MongoClient("{mongodb url}")
    users_collection = client.get_collection("Users")
    if users_collection.find_one({"username": username}):
        return 1
    else:
        return 0

def add_user(username, password, recovery_email):
    client = MongoClient("{mongodb url}")
    users_collection = client.get_collection("Users")
    if check_user(username, password, recovery_email) == 0:
        users_collection.insert_one({"username":username, "password":password, "email":recovery_email})
        return "User successfully added"
    else:
        return "User already exists"

def authenticate_user(username, password):
    client = MongoClient("{mongodb url")
    users_collection = client.get_collection("Users")
    doc = users_collection.find_one({"username":username})
    if doc:
        if doc["password"] == password:
            return 1
        else:
            return 0
    else:
        return 0



