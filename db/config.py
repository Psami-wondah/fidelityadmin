from pymongo import MongoClient
from utils.config import MONGO_URI

conn = MongoClient(MONGO_URI, connect=False)

db = conn.okorie
