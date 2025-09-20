import os
from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# get password and uri for database connection
load_dotenv()
db_password = os.getenv('MONGO_PASSWORD')
uri = os.getenv('DATABASE_URI').replace('db_password', db_password)

# create client and connect to server
client = MongoClient(uri, server_api=ServerApi('1'))

# ping for confirmation and update databases
db = client['bigcat']
