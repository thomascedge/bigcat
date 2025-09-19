import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api import register_routes

app = FastAPI()
register_routes(app)

origins = [
    'http://localhost:8000',
    'https://bigcat.thomascedge.com'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

@app.get('/')
def startup():
    return {'healthcheck': 'OK'}

if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=8000)