from fastapi import FastAPI
from app.auth.controller import router as auth_router
from app.users.controller import router as users_router
from app.concerts.controller import router as concerts_router
from app.seats.controller import router as seats_router
from app.bookings.controller import router as bookings_router

def register_routes(app: FastAPI):
    app.include_router(auth_router)
    app.include_router(users_router)
    app.include_router(concerts_router)
    app.include_router(seats_router)
    app.include_router(bookings_router)