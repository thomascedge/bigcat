import uvicorn
from fastapi import FastAPI
from mangum import Mangum
from app.api import register_routes
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
register_routes(app)
handler = Mangum(app)

# adding middleware for 
origins = [
    "http://localhost:3000",           # dev
    "https://bigcat.thomascedge.com",  # prod
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/')
def startup():
    return {'healthcheck': 'OK'}

if __name__ == '__main__':
    uvicorn.run("run_server:app", host="0.0.0.0", port=8000, reload=True)
