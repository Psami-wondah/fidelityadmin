from pymongo import MongoClient
from utils.config import MONGO_URI

conn = MongoClient(MONGO_URI, connect=False)

db = conn.okorie


# def approve_admin():
#     user = db.admins.find_one_and_update({"username": "chima"}, {"$set": {""}})
