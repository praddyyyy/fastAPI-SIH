import imp
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()
MONGODB = os.getenv("MONGODB_URI")
client = MongoClient(MONGODB)

db = client.test

collection = db.users
collection_institutes = db.institutes