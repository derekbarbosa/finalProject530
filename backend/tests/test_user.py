import pytest
import os
import logging
import pymongo

from dotenv import load_dotenv
from pymongo import MongoClient
from .. import user_module as user

load_dotenv()

DB_PASS = os.environ.get("MONGO_DB_PASS")

def test_check_user():
    test_username = "test"
    test_email = "test@email"
    test_pass = "testpass"
    assert(user.check_user(test_username, test_pass, test_email) == 1)
    logging.info("check user test passed")
    pass

def test_add_user():
    test_username = "test1"
    test_email = "test1@email"
    test_pass = "test1pass"
    
    user.add_user(test_username, test_pass, test_email)

    client = MongoClient(f"mongodb+srv://EC530_TTY:{DB_PASS}@cluster0.ds0t5.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
    db = client["TTY"]
    user_collection = db["Users"]
    assert(user_collection.find_one({"username":test_username, "password":test_pass, "email":test_email}) == 1)
    logging.info("add user test passed")
    user_collection.delete_one({"username":test_username})

def test_authenticate_user():
    test_username = "peter"
    test_email = "peter@email"
    test_pass = "urmom"

    client = MongoClient(f"mongodb+srv://EC530_TTY:{DB_PASS}@cluster0.ds0t5.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
    db = client["TTY"]
    user_collection = db["Users"]
    doc = user_collection.find_one({"username":test_username})
    assert(doc["password"] == test_pass)
    logging.info("authenticate user test passed")
    pass

    if __name__ == '__main__':
        test_check_user()
        test_add_user()
        test_authenticate_user()
        print("All user module tests passed")
