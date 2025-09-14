from fastapi import Depends
from typing import Optional
from pymongo.database import Database
from src.auth.model import TokenData
from src.database.core import get_database
from src.concerts.model import *
from src.exceptions import ConcertNotFoundError, ConcertCreationError
from src.logging import logger

def get_concert_by_id(concert_id: str, db: Database = Depends(get_database)) -> Concert:
    concert = db['concert'].find_one({'uid': concert_id})
    if not concert:
        logger.warning(f'Concert not found with concert_id: {concert_id}')
        raise ConcertNotFoundError(concert_id)
    logger.info(f'Retrieved concert {concert_id}.')
    return Concert(**concert)

def get_all_concerts(db: Database=Depends(get_database)) -> ConcertResponse:
    concert_list = [Concert(**concert) for concert in db['concert'].find()]
    logger.info(f'Retrieved {len(concert_list)} concerts.')
    return ConcertResponse(concert_list=concert_list)

def search_concerts(concert_id: Optional[str]=None, 
                    artist: Optional[str]=None, 
                    tour_name: Optional[str]=None,
                    venue: Optional[str]=None,
                    location: Optional[str]=None,
                    concert_datetime: Optional[datetime]=None, 
                    db: Database=Depends(get_database)) -> ConcertResponse:
    """
    Searches database for concert data based on given query. It is assumed that a concert_id
    will not be searched with an artist, venue, location, or date.
    Example query: /concert/?artist=Juliana+Huxtable&date=2025-09-05T22:30:00

    :param optional str concert_id: concert id
    :param optional str artist: artist name
    :param optional str venue: venue name
    :param optional str location: location
    :param optional datetime datetime: datetime object
    :return: list of concert objects
    :raises: ConcertNotFoundError
    """
    if concert_id:
        query = {'uid': concert_id}
    else:
        # format date to datetime and get date range for querying
        if concert_datetime:
            concert_datetime = concert_datetime.strftime('%m-%d-%Y')
            start_date = datetime.strptime(f'{concert_datetime} 00:00', '%m-%d-%Y %H:%M') 
            end_date = datetime.strptime(f'{concert_datetime} 23:59', '%m-%d-%Y %H:%M')

        if not artist and not tour_name and not venue and not location and concert_datetime:
            query = {'concert_datetime': {"$gte": start_date, "$lte": end_date}}
        elif not artist and not tour_name and not venue and location and not concert_datetime:
            query = {'location': {'$regex': location, '$options': 'i'}}
        elif not artist and not tour_name and not venue and location and concert_datetime:
            query = {'$or': [{'location': {'$regex': location, '$options': 'i'}}, {'concert_datetime': {"$gte": start_date, "$lte": end_date}}]}
        elif not artist and not tour_name and venue and not location and not concert_datetime:
            query = {'venue': {'$regex': venue, '$options': 'i'}}
        elif not artist and not tour_name and venue and not location and concert_datetime:
            query = {'$or': [{'venue': {'$regex': venue, '$options': 'i'}}, {'concert_datetime': {"$gte": start_date, "$lte": end_date}}]}
        elif not artist and not tour_name and venue and location and not concert_datetime:
            query = {'$or': [{'venue': {'$regex': venue, '$options': 'i'}}, {'location': {'$regex': location, '$options': 'i'}}]}
        elif not artist and not tour_name and venue and location and concert_datetime:
            query = {'$or': [{'venue': {'$regex': venue, '$options': 'i'}}, {'location': {'$regex': location, '$options': 'i'}}, {'concert_datetime': {"$gte": start_date, "$lte": end_date}}]}
        elif not artist and tour_name and not venue and not location and not concert_datetime:
            query = {'tour_name': {'$regex': tour_name, '$options': 'i'}}
        elif not artist and tour_name and not venue and not location and concert_datetime:
            query = {'$or': [{'tour_name': {'$regex': tour_name, '$options': 'i'}}, {'concert_datetime': {"$gte": start_date, "$lte": end_date}}]}
        elif not artist and tour_name and not venue and location and not concert_datetime:
            query = {'$or': [{'tour_name': {'$regex': tour_name, '$options': 'i'}}, {'location': {'$regex': location, '$options': 'i'}}]}
        elif not artist and tour_name and not venue and location and concert_datetime:
            query = {'$or': [{'tour_name': {'$regex': tour_name, '$options': 'i'}}, {'location': {'$regex': location, '$options': 'i'}}, {'concert_datetime': {"$gte": start_date, "$lte": end_date}}]}
        elif not artist and tour_name and venue and not location and not concert_datetime:
            query = {'$or': [{'tour_name': {'$regex': tour_name, '$options': 'i'}}, {'venue': {'$regex': venue, '$options': 'i'}}]}
        elif not artist and tour_name and venue and not location and concert_datetime:
            query = {'$or': [{'tour_name': {'$regex': tour_name, '$options': 'i'}}, {'venue': {'$regex': venue, '$options': 'i'}}, {'concert_datetime': {"$gte": start_date, "$lte": end_date}}]}
        elif not artist and tour_name and venue and location and not concert_datetime:
            query = {'$or': [{'tour_name': {'$regex': tour_name, '$options': 'i'}}, {'venue': {'$regex': venue, '$options': 'i'}}, {'location': {'$regex': location, '$options': 'i'}}]}
        elif not artist and tour_name and venue and location and concert_datetime:
            query = {'$or': [{'tour_name': {'$regex': tour_name, '$options': 'i'}}, {'venue': {'$regex': venue, '$options': 'i'}}, {'location': {'$regex': location, '$options': 'i'}}, {'concert_datetime': {"$gte": start_date, "$lte": end_date}}]}
        elif artist and not tour_name and not venue and not location and not concert_datetime:
            query = {'artist': {'$regex': artist, '$options': 'i'}}
        elif artist and not tour_name and not venue and not location and concert_datetime:
            query = {'$or': [{'artist': {'$regex': artist, '$options': 'i'}}, {'concert_datetime': {"$gte": start_date, "$lte": end_date}}]}
        elif artist and not tour_name and not venue and location and not concert_datetime:
            query = {'$or': [{'artist': {'$regex': artist, '$options': 'i'}}, {'location': {'$regex': location, '$options': 'i'}}]}
        elif artist and not tour_name and not venue and location and concert_datetime:
            query = {'$or': [{'artist': {'$regex': artist, '$options': 'i'}}, {'location': {'$regex': location, '$options': 'i'}}, {'concert_datetime': {"$gte": start_date, "$lte": end_date}}]}
        elif artist and not tour_name and venue and not location and not concert_datetime:
            query = {'$or': [{'artist': {'$regex': artist, '$options': 'i'}}, {'venue': {'$regex': venue, '$options': 'i'}}]}
        elif artist and not tour_name and venue and not location and concert_datetime:
            query = {'$or': [{'artist': {'$regex': artist, '$options': 'i'}}, {'venue': {'$regex': venue, '$options': 'i'}}, {'concert_datetime': {"$gte": start_date, "$lte": end_date}}]}
        elif artist and not tour_name and venue and location and not concert_datetime:
            query = {'$or': [{'artist': {'$regex': artist, '$options': 'i'}}, {'venue': {'$regex': venue, '$options': 'i'}}, {'location': {'$regex': location, '$options': 'i'}}]}
        elif artist and not tour_name and venue and location and concert_datetime:
            query = {'$or': [{'artist': {'$regex': artist, '$options': 'i'}}, {'venue': {'$regex': venue, '$options': 'i'}}, {'location': {'$regex': location, '$options': 'i'}}, {'concert_datetime': {"$gte": start_date, "$lte": end_date}}]}
        elif artist and tour_name and not venue and not location and not concert_datetime:
            query = {'$or': [{'artist': {'$regex': artist, '$options': 'i'}}, {'tour_name': {'$regex': tour_name, '$options': 'i'}}]}
        elif artist and tour_name and not venue and not location and concert_datetime:
            query = {'$or': [{'artist': {'$regex': artist, '$options': 'i'}}, {'tour_name': {'$regex': tour_name, '$options': 'i'}}, {'concert_datetime': {"$gte": start_date, "$lte": end_date}}]}
        elif artist and tour_name and not venue and location and not concert_datetime:
            query = {'$or': [{'artist': {'$regex': artist, '$options': 'i'}}, {'tour_name': {'$regex': tour_name, '$options': 'i'}}, {'location': {'$regex': location, '$options': 'i'}}]}
        elif artist and tour_name and not venue and location and concert_datetime:
            query = {'$or': [{'artist': {'$regex': artist, '$options': 'i'}}, {'tour_name': {'$regex': tour_name, '$options': 'i'}}, {'location': {'$regex': location, '$options': 'i'}}, {'concert_datetime': {"$gte": start_date, "$lte": end_date}}]}
        elif artist and tour_name and venue and not location and not concert_datetime:
            query = {'$or': [{'artist': {'$regex': artist, '$options': 'i'}}, {'tour_name': {'$regex': tour_name, '$options': 'i'}}, {'venue': {'$regex': venue, '$options': 'i'}}]}
        elif artist and tour_name and venue and not location and concert_datetime:
            query = {'$or': [{'artist': {'$regex': artist, '$options': 'i'}}, {'tour_name': {'$regex': tour_name, '$options': 'i'}}, {'venue': {'$regex': venue, '$options': 'i'}}, {'concert_datetime': {"$gte": start_date, "$lte": end_date}}]}
        elif artist and tour_name and venue and location and not concert_datetime:
            query = {'$or': [{'artist': {'$regex': artist, '$options': 'i'}}, {'tour_name': {'$regex': tour_name, '$options': 'i'}}, {'venue': {'$regex': venue, '$options': 'i'}}, {'location': {'$regex': location, '$options': 'i'}}]}
        elif artist and tour_name and venue and location and concert_datetime:
            query = {'$or': [{'artist': {'$regex': artist, '$options': 'i'}}, {'tour_name': {'$regex': tour_name, '$options': 'i'}}, {'venue': {'$regex': venue, '$options': 'i'}}, {'location': {'$regex': location, '$options': 'i'}}, {'concert_datetime': {"$gte": start_date, "$lte": end_date}}]}
        
    concert_list = [Concert(**concert) for concert in db['concert'].find(query)]

    if len(concert_list) != 0:
        logger.info(f'Retrieved {len(concert_list)} concerts.')
        return ConcertResponse(concert_list=concert_list)
    else:
        logger.warning(f'No concert found.')
        raise ConcertNotFoundError()    
    
def create_concert(current_user: TokenData, concert: Concert, db: Database = Depends(get_database)) -> Concert:
    try:
        db['concert'].insert_one(concert.model_dump())
        logger.info(f'Created new concert with id {concert.uid}. Created by {current_user.uid}.')
        return get_concert_by_id(concert.uid, db)
    except Exception as e:
        logger.error(f'Failed to create concert. Error {str(e)}')
        raise ConcertCreationError(str(e))
    
def update_concert(current_user: TokenData, concert_id: str, concert_update: Concert, db: Database = Depends(get_database)) -> Concert:
    db['concert'].update_many({'uid': concert_id}, {'$set': concert_update.model_dump()})
    logger.info(f'Concert {concert_update.uid} successfully updated. Updated by {current_user.uid}')
    return get_concert_by_id(concert_update.uid, db)

def cancel_concert(current_user: TokenData, concert_id: str, db: Database = Depends(get_database)) -> Concert:
    db['concert'].update_one({'uid': concert_id}, {'$set': {'status': ConcertStatus.CANCELED.value}})
    logger.debug(concert_id)
    logger.info(f'Concert {concert_id} CANCELED. CANCELED by {current_user.uid}')
    return get_concert_by_id(concert_id, db)
