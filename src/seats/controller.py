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

@router.get('/test/{seat}')
def testing(seat: str):
    from src.logging import logger
    logger.debug(f'{seat}')

@router.get('/{seat_id}', response_model=model.Seat)
def get_seat_by_id(seat_id: str, db: DbSession):
    return service.get_seat_by_id(seat_id, db)

@router.get('/', response_model=model.SeatResponse)
def search_seats(db: DbSession, 
                  concert_id: Optional[str]|None=None,
                  venue: Optional[str]|None=None):
    return service.search_seats(concert_id, venue, db)

@router.post('/', response_model=model.SeatResponse, status_code=status.HTTP_201_CREATED)
def create_seats(current_user: CurrentUser, db: DbSession, seats: model.SeatRequest):
    return service.create_seats(current_user, seats, db)

@router.put('/edit/{seat_id}')
def edit_seat(current_user: CurrentUser, seat_id: str, seat_update: model.Seat, db: DbSession):
    return service.edit_seat(current_user, seat_id, seat_update, db)

@router.delete('/{seat_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_seat(current_user: CurrentUser, seat_id: str, db: DbSession):
    return service.delete_seat(current_user, seat_id, db)
