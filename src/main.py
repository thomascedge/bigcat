import uvicorn
from fastapi import FastAPI
from api import register_routes
from mangum import Mangum

app = FastAPI()
register_routes(app)
handler = Mangum(app)

@app.get('/')
def startup():
    return {'healthcheck': 'OK'}

if __name__ == '__main__':
    uvicorn.run("run_server:app", host="0.0.0.0", port=8000, reload=True)
