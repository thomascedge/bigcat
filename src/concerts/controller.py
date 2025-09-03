from fastapi import APIRouter, Depends, status
from pymongo.database import Database
from datetime import datetime
from typing import Optional
from src.concerts import model
from src.concerts import service
from src.database.core import DbSession

router = APIRouter(
    prefix='/concerts',
    tags=['Concerts']
)

@router.get('/', response_model=model.ConcertResponse)
def get_all_concerts(db: DbSession):
    return service.get_all_concerts(db)

@router.get('/{concert_id}', response_model=model.Concert)
def get_concert_(concert_id: str, db: DbSession):
    return service.get_concert_by_id(concert_id, db)


@router.get('/search', response_model=model.ConcertResponse)
def search_concerts(db: DbSession,
                    concert_id: Optional[str] = None,
                    artist: Optional[str] = None, 
                    venue: Optional[str] = None,
                    location: Optional[str] = None, 
                    date: Optional[datetime] = None):
    return service.serach_concerts(concert_id, artist, venue, location, date, db)

@router.post('/', status_code=status.HTTP_200_OK)
def create_concert(concert: model.Concert, db: DbSession):
    return service.create_concert(concert, db)

@router.patch('/{concert_id}', response_class=model.ConcertResponse)
def update_concert(concert_id: str, concert_update: model.Concert, db: DbSession):
    return service.update_concert(concert_id, concert_update, db)

@router.delete('/{concert_id}', status_code=status.HTTP_202_ACCEPTED)
def cancel_concert(concert_id: str, db: DbSession):
    service.cancel_concert(concert_id, db)
