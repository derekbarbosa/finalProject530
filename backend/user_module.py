from pymongo import MongoClient

def add_user(username, password, recovery_email):
    client = MongoClient("{mongodb url}")
    users_collection = client.get_collection("Users")
    if not users_collection.find({"username": username}):
        users_collection.insert_one({"username": username, "password": password, "email": recovery_email})
        return 1
    else:
        return 0

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



