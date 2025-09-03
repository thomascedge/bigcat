import os
import certifi
from fastapi import Depends
from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from pymongo.database import Database
from typing import Annotated
from src.logging import logger

load_dotenv()

db_password = os.getenv('MONGO_PASSWORD')
uri = os.getenv('DATABASE_URI').replace('db_password', db_password)
client = MongoClient(uri, server_api=ServerApi('1'), tlsCAFile=certifi.where())
logger.info(f'Successfully connected to bigcat database.')

def get_database():
    """
    Returns database
    """
    db = client['bigcat']

    try:
        yield db
    finally: 
        client.close()

DbSession = Annotated[Database, Depends(get_database)]
