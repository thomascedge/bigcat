from fastapi import APIRouter, Depends, status
from pymongo.database import Database
from datetime import datetime
from typing import Optional
from src.concerts import model
from src.concerts import service
from src.database.core import DbSession
from src.auth.service import CurrentUser

router = APIRouter(
    prefix='/concerts',
    tags=['Concerts']
)

@router.get('/', response_model=model.ConcertResponse)
def get_all_concerts(db: DbSession):
    return service.get_all_concerts(db)

@router.get('/id/{concert_id}', response_model=model.Concert)
def get_concert(concert_id: str, db: DbSession):
    return service.get_concert_by_id(concert_id, db)

@router.get('/search', response_model=model.ConcertResponse)
def search_concerts(db: DbSession,
                    concert_id: Optional[str] = None,
                    artist: Optional[str] = None, 
                    tour_name: Optional[str]=None,
                    venue: Optional[str] = None,
                    location: Optional[str] = None, 
                    concert_datetime: Optional[datetime] = None):
    return service.search_concerts(concert_id, artist, tour_name, venue, location, concert_datetime, db)

@router.post('/', response_model=model.Concert, status_code=status.HTTP_201_CREATED)
def create_concert(current_user: CurrentUser, concert: model.Concert, db: DbSession):
    return service.create_concert(current_user, concert, db)

@router.patch('/{concert_id}', response_class=model.Concert)
def update_concert(current_user: CurrentUser, concert_id: str, concert_update: model.Concert, db: DbSession):
    return service.update_concert(current_user, concert_id, concert_update, db)

@router.patch('/cancel/{concert_id}', status_code=status.HTTP_202_ACCEPTED)
def cancel_concert(current_user: CurrentUser, concert_id: str, db: DbSession):
    service.cancel_concert(current_user, concert_id, db)
