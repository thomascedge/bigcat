from fastapi import APIRouter, Depends
from pymongo.database import Database
from src.bookings import model
from src.bookings import service
from src.database.core import get_database
from src.auth.service import CurrentUser
from src.database.core import DbSession

router = APIRouter(
    prefix='/bookings',
    tags=['Bookings']
)

@router.get('/', response_model=model.BookingResponse)
def get_bookings(current_user: CurrentUser, db: DbSession):
    return service.get_bookings(current_user, db)

@router.get('/{booking_id}', response_model=model.BookingResponse)
def get_booking(current_user: CurrentUser, db: DbSession):
    return service.get_booking(current_user, db)

# @router.post('/', )
# def book_tickets(user_id: str=Body(...), concert_id: str=Body(...), seats: List[str]=Body(...)) -> Booking:

# @router.patch('/booking/{booking_id}')
# async def cancel_booking(booking_id: str) -> str: