## mongodb username: EC530_TTY

import pymongo
import dotenv
import os

from pymongo import MongoClient

load_dotenv()

DB_PASS = os.environ.get("MONGO_DB_PASS")

def check_user(username, password, recovery_email):
    client = MongoClient(f"mongodb+srv://EC530_TTY:{DB_PASS}@cluster0.ds0t5.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
    db = client["TTY"]
    users_collection = db["Users"]
    if users_collection.find_one({"username": username}):
        return 1
    else:
        return 0

def add_user(username, password, recovery_email):
    client = MongoClient(f"mongodb+srv://EC530_TTY:{DB_PASS}@cluster0.ds0t5.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
    db = client["TTY"]
    users_collection = db["Users"]
    if check_user(username, password, recovery_email) == 0:
        users_collection.insert_one({"username":username, "password":password, "email":recovery_email})
        return "User successfully added"
    else:
        return "User already exists"

def authenticate_user(username, password):
    client = MongoClient(f"mongodb+srv://EC530_TTY:{DB_PASS}@cluster0.ds0t5.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
    db = client["TTY"]
    users_collection = db["Users"]
    doc = users_collection.find_one({"username":username})
    if doc:
        if doc["password"] == password:
            return 1
        else:
            return 0
    else:
        return 0
