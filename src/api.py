from fastapi import FastAPI
from src.auth.controller import router as auth_router
from src.users.controller import router as users_router
from src.concerts.controller import router as concerts_router
from src.seats.controller import router as seats_router

def register_routes(app: FastAPI):
    app.include_router(auth_router)
    app.include_router(users_router)
    app.include_router(concerts_router)
    app.include_router(seats_router)
    