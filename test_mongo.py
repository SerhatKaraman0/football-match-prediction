
from pymongo.mongo_client import MongoClient
from dotenv import load_dotenv
import os 

load_dotenv()

DB_PWD = os.getenv("MONGO_DB_PASSWORD")
DB_URI = os.getenv("MONGO_DB_URI")

if DB_PWD is None:
    raise ValueError("MONGO_DB_URI environment variable is not set")

uri = DB_URI

client = MongoClient(uri)

try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)