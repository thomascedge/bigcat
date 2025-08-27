import os
from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
# from util.data.codec import TYPE_REGISTRY

load_dotenv()

db_password = os.getenv('MONGO_PASSWORD')
uri = os.getenv('DATABASE_URI').replace('db_password', db_password)

client = MongoClient(uri, server_api=ServerApi('1'))

try:
    client.admin.command('ping')
    print("Successfully connected to MongoDB!")

except Exception as exception:
    print(exception)
