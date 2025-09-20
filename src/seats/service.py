from fastapi import Depends
from typing import Optional
from pymongo.database import Database
from uuid import uuid4
from database.core import get_database
from auth.model import TokenData
from seats.model import *
from exceptions import SeatNotFoundError, SeatCreationError, NoAdminPermissions
from loguru_log import logger


def get_seat_by_id(seat_id: str, db: Database=Depends(get_database)) -> Seat:
    seat = db['seat'].find_one({'uid': seat_id})
    if not seat:
        logger.warning(f'Seat not found with seat_id: {seat_id}')
        raise SeatNotFoundError(seat_id)
    logger.info(f'Retrieved seat {seat_id}.')
    return Seat(**seat)

def search_seats(concert_id: str|None= None, venue: str|None= None, db: Database=Depends(get_database)) -> SeatResponse:
    if concert_id or venue:
        if concert_id and not venue:
            query = {'concert_id': concert_id}
        elif not concert_id and venue:
            query = {'venue': venue}
        elif concert_id and venue:
            query = {'$or': [{'concert_id': concert_id}, {'venue': venue}]}

        seat_list = [Seat(**seat) for seat in db['seat'].find(query)]

        if len(seat_list) != 0:
            logger.info(f'Retrieved {len(seat_list)} seats.')
            return SeatResponse(seat_list=seat_list)
        else:
            logger.warning(f'No seat found.')
            raise SeatNotFoundError() 
    else:
        seat_list = [Seat(**seat) for seat in db['seat'].find()]
        logger.info(f'Retrieved {len(seat_list)} seats.')
        return SeatResponse(seat_list=seat_list)

def create_seats(current_user: TokenData, seats: SeatRequest, db: Database=Depends(get_database)) -> SeatResponse:
    if not current_user.admin:
        raise NoAdminPermissions()
    
    try:
        for seat in seats.seat_list:
            if seat.uid == '' or seat.uid == None:
                seat.uid = str(uuid4())

            db['seat'].insert_one(seat.model_dump())
            logger.info(f'Created new seat with id {seat.uid}. Created by {current_user.uid}.')
        return SeatResponse(seat_list=seats.seat_list)
    except Exception as e:
        logger.error(f'Failed to create seat. Error {str(e)}')
        raise SeatCreationError(str(e))
    
def edit_seat(current_user: TokenData, seat_id: str, seat_update: Seat, db: Database=Depends(get_database)) -> Seat:
    if not current_user.admin:
        raise NoAdminPermissions()

    db['seat'].update_one(
        {'uid': seat_id}, 
        {'$set': {
            'concert_id': seat_update.concert_id,
            'venue': seat_update.venue,
            'seat_number': seat_update.seat_number,
            'seat_type': seat_update.seat_type,
            'price': seat_update.price,
            'status': seat_update.status
        }}
    )
    logger.info(f'Seat {seat_id} successfully updated. Created by {current_user.uid}')
    return get_seat_by_id(seat_id, db)

def delete_seat(current_user: TokenData, seat_id: str, db: Database=Depends(get_database)) -> None:
    if not current_user.admin:
        raise NoAdminPermissions()
    
    db['seat'].delete_one({'uid': seat_id})
    logger.info(f'Seat {seat_id} removed by {current_user.uid}.')
