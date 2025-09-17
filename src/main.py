from fastapi import FastAPI
from src.api import register_routes

app = FastAPI()
register_routes(app)

@app.get('/')
def startup():
    return {'healthcheck': 'OK'}