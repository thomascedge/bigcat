from fastapi import APIRouter, status
from src.bookings import model
from src.bookings import service
from src.auth.service import CurrentUser
from src.database.core import DbSession

router = APIRouter(
    prefix='/bookings',
    tags=['Bookings']
)

@router.get('/', response_model=model.BookingResponse)
def get_all_bookings(current_user: CurrentUser, db: DbSession):
    return service.search_booking(current_user, db)

@router.get('/search', response_model=model.BookingResponse)
def search_booking(current_user: CurrentUser,
                   db: DbSession, 
                   booking_id: str|None=None, 
                   venue: str|None=None):
    return service.search_booking(current_user, booking_id, venue, db)

@router.post('/', status_code=status.HTTP_201_CREATED)
def book_tickets(current_user: CurrentUser, request: model.BookingRequest, db: DbSession):
    return service.book_tickets(current_user, request.concert_id, request.seat_list, db)

@router.patch('/{booking_id}/add/{seat_id}')
def add_seat_to_booking(current_user: CurrentUser, booking_id: str, seat_id: str, db: DbSession):
    return service.add_seat_to_booking(current_user, booking_id, seat_id, db)

@router.patch('/{booking_id}/remove/{seat_id}')
def remove_seat_from_booking(current_user: CurrentUser, booking_id: str, seat_id: str, db: DbSession):
    return service.remove_seat_from_booking(current_user, booking_id, seat_id, db)

@router.patch('/{booking_id}/cancel')
def cancel_booking(current_user: CurrentUser, booking_id: str, db: DbSession):
    return service.cancel_booking(current_user, booking_id, db)

@router.put('/')
def edit_booking(current_user: CurrentUser, update_request: model.UpdateBookingRequest, db: DbSession):
    return service.edit_booking(current_user, update_request.booking_id, update_request.booking_update, db)
