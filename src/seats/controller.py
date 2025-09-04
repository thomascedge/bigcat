from fastapi import APIRouter, status
from src.seats import model
from src.seats import service
from src.database.core import DbSession
from src.auth.service import CurrentUser
from typing import Optional

router = APIRouter(
    prefix='/seats',
    tags=['Seats']
)

@router.get('/', response_model=model.SeatResponse)
def search_seats(db: DbSession, 
                  concert_id: Optional[str]|None=None,
                  venue: Optional[str]|None=None):
    return service.search_seats(concert_id, venue, db)

@router.post('/', status_code=status.HTTP_200_OK)
def create_seats(db: DbSession, seats=list[model.Seat]):
    return service.create_seats(seats, db)

@router.patch('/edit/{seat_id}')
def edit_seat(seat_id: str, seat_update: model.Seat, db: DbSession):
    return service.edit_seat(seat_id, seat_update, db)

@router.delete('/{seat_id}')
def delete_seat(seat_id: str, db: DbSession):
    return service.delete_seat(seat_id, db)
