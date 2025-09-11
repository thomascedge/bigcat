from fastapi import Depends
from pymongo.database import Database
from uuid import uuid4
from datetime import datetime
from src.bookings.model import *
from src.seats.model import SeatStatus
from src.exceptions import BookingNotFoundError
from src.auth.model import TokenData
from src.database.core import get_database
from src.exceptions import (
    BookingNotFoundError, 
    BookingCreationError,
    BookingAlreadyUpdatedError,
    BookingUpdateCode,
    ConcertNotFoundError, 
    SeatUnavailableError
)
from src.logging import logger

def get_booking_by_id(current_user: TokenData, booking_id: str, db: Database=Depends(get_database)) -> Booking:
    booking = db['booking'].find_one({'uid': booking_id})
    if booking is None:
        raise BookingNotFoundError(booking_id)
    logger.info(f'Retrieved booking {booking_id} for user {current_user.uid}')
    
    if booking['seats'] == None:
        booking['seats'] = []
    return Booking(**booking)

def search_booking(current_user: TokenData, booking_id: str|None=None, venue: str|None=None, db: Database=Depends(get_database)) -> BookingResponse:
    if booking_id or venue:
        if booking_id and not venue:
            query = {'uid': booking_id}
        elif not booking_id and venue:
            query = {'venue': venue}

        booking_list = [Booking(**booking) for booking in db['booking'].find(query)]
        
        if len(booking_list) != 0:
            logger.info(f'Retrieved {len(booking_list)} bookings.')
            return BookingResponse(booking_list=booking_list)
        else:
            logger.warning(f'No booking found.')
            raise BookingNotFoundError() 
    else:
        bookings_list = [booking for booking in db['bookings'].find({'uid': current_user.uid})] 
        logger.info(f'Retrieved {len(bookings_list)} bookings for user {current_user.uid}')
        return BookingResponse(booking_list=bookings_list)

def book_tickets(current_user: TokenData, concert_id: str, seat_ids: list[str], db: Database=Depends(get_database)) -> Booking:
    try:
        # check if concert exists
        concert = db['concert'].find_one({'concert_id': concert_id})
        if concert is None:
            raise ConcertNotFoundError(concert_id=concert_id)
        
        total_price = 0
        str_seat_list = []

        for seat_id in seat_ids:
            seat_id = str(seat_id)
            seat = db['seat'].find_one({'uid': seat_id})

            # check seat availability 
            if seat is None:
                raise SeatUnavailableError()
            elif seat['status'] == SeatStatus.BOOKED.value:
                raise SeatUnavailableError(uid=seat.uid)
            else:
                # find seat and add total price
                seat = db['seat'].find_one_and_update({"uid": seat_id}, {"$set": {"status": SeatStatus.BOOKED.value}})
                total_price += seat['price']
                str_seat_list.append(seat_id)

        # create booking if successful and return booking id
        current_datetime = datetime.now()
        venue = concert['venue']

        booking = Booking(
            uid=str(uuid4()),
            user_id=str(current_user.uid),
            concert_id=concert_id,
            venue=venue,
            seats=str_seat_list,
            total_price=total_price,
            payment_status=PaymentStatus.PENDING.value,
            status=BookingStatus.CONFIRMED.value,
            request_datetime=current_datetime,
            update_datetime=current_datetime,
            confirmation_id=str(uuid4())[:8]
        )

        db['booking'].insert_one(booking.model_dump())
        logger.info(f'Created new booking with id {booking.uid}. Created by {current_user.uid}.')
        return get_booking_by_id(current_user, booking.uid, db)
    except Exception as e:
        logger.error(f'Failed to create booking. Error {str(e)}')
        raise BookingCreationError(str(e))

def add_seat_to_booking(current_user: TokenData, booking_id: str, seat_id: str, db: Database=Depends(get_database)) -> Booking:
    # find booking 
    booking = get_booking_by_id(current_user, booking_id, db)

    if booking is None:
        raise BookingNotFoundError(booking_id)

    # check if booking already added
    if seat_id in booking.seats:
        raise BookingAlreadyUpdatedError(booking_id=booking_id, seat_id=seat_id, code=BookingUpdateCode.SEAT_ADDED)

    # update booking and datetime
    seats_list = booking.seats
    seats_list.append(seat_id)
    
    db['booking'].update_one({"uid": booking_id}, {"$set": {'seats': seats_list, 'update_datetime': datetime.now()}})

    # update seat
    db['seat'].find_one_and_update({"uid": seat_id}, {"$set": {"status": SeatStatus.BOOKED.value}})

    logger.info(f'Seat {seat_id} added to booking {booking_id}. Updated by {current_user.uid}')
    return get_booking_by_id(current_user, booking_id, db)

def remove_seat_from_booking(current_user: TokenData, booking_id:str, seat_id: str, db: Database=Depends(get_database)) -> Booking:
    # find and update booking datetime
    booking = get_booking_by_id(current_user, booking_id, db)

    if booking is None:
        raise BookingNotFoundError(booking_id)
    
    # check if booking already removed
    if seat_id not in booking.seats:
        raise BookingAlreadyUpdatedError(booking_id=booking_id, seat_id=seat_id, code=BookingUpdateCode.SEAT_REMOVED)

    # update booking and datetime
    seats_list = booking.seats
    seats_list.remove(seat_id)
    db['booking'].update_one({"uid": booking_id}, {"$set": {'seats': seats_list, 'update_datetime': datetime.now()}})

    # update seat
    db['seat'].find_one_and_update({"uid": seat_id}, {"$set": {"status": SeatStatus.AVAILABLE.value}})

    logger.info(f'Seat {seat_id} added to booking {booking_id}. Updated by {current_user.uid}')
    return get_booking_by_id(current_user, booking_id, db)

def cancel_booking(current_user: TokenData, booking_id: str, db: Database=Depends(get_database)) -> Booking:
    """
    Cancels a booking for a given booking_id. Does not delete the booking in the 
    database, instead releases the seats booked and changes booking status to 
    canceled.

    :param str booking_id: a booking id
    :return: message confirming cancelation
    :raises: 400 error if booking already canceled
    :raises: 404 error if booking_id not found
    """
    # find and update booking status to canceled
    booking = db['booking'].find_one_and_update({"uid": booking_id}, {"$set": {"status": BookingStatus.CANCELED.value, 'update_datetime': datetime.now()}})

    if booking is None:
        raise BookingNotFoundError(booking_id)

    # check if booking already canceled
    if booking['status'] == BookingStatus.CANCELED.value:
        raise BookingAlreadyUpdatedError(booking_id, BookingUpdateCode.CANCELED)

    # get all seats in a booking and update status to available
    for seat_id in booking['seats']:
        db['seat'].find_one_and_update({"uid": seat_id}, {"$set": {"status": SeatStatus.AVAILABLE.value}})

    logger.info(f'Booking {booking_id} canceled and seats released. Updated by {current_user.uid}')
    return get_booking_by_id(current_user, booking_id, db)

def edit_booking(current_user: TokenData, booking_id: str, booking_update: Booking, db: Database=Depends(get_database)) -> Booking:
    db['booking'].update_one(
        {'uid': booking_id}, 
        {'$set':{
            'user_id': booking_update.user_id,
            'concert_id': booking_update.concert_id,
            'venue': booking_update.venue,
            'seats': booking_update.seats,
            'total_price': booking_update.total_price,
            'payment_status': booking_update.payment_status,
            'status': booking_update.status,
            'update_datetime': datetime.now()
        }}
    )
    logger.info(f'Booking {booking_id} successfully updated. Created by {current_user.uid}')
    return get_booking_by_id(current_user, booking_id, db)
