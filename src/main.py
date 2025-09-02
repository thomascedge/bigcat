from fastapi import FastAPI
from src.api import register_routes

app = FastAPI()
register_routes(app)