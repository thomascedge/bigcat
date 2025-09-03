from fastapi import FastAPI, HTTPException, Body, Depends
from pymongo.database import Database
from bson.objectid import ObjectId
from collections import OrderedDict
from src.bookings import model
from src.exceptions import BookingNotFoundError
from src.auth.model import TokenData
from src.database.core import get_database
from src.logging import logger

# internal cache checking for number of seats available for a given concert 
# with GA seats. { concert_id : capacity }
# def _populate_cache() -> dict:
#     """
#     Populates internal cache with number of total GA seats available for a given concert.
#     Uses equivalent SQL query to
#         SELECT 
#             concert_id,
#             COUNT(concert_id) as available_seats
#         FROM seat
#         GROUP BY concert_id
#         HAVING seat_number = 'GA' AND
#             status = 0
        
#     :returns: dictionary with format { concert_id : avaliable_seats }
#     """
#     cache = {}

#     filter_on = {'$match': {'seat_number': 'GA', 'status': SeatStatus.AVAILABLE.value}}
#     group_by_concert_id = {'$group': {'_id': '$concert_id', 'count': {'$sum': 1}}}
#     pipeline = [filter_on, group_by_concert_id]
#     results = list(SEAT_DB.aggregate(pipeline=pipeline))

#     for doc in results:
#         cache[doc['_id']] = doc['count']

#     return cache

# seats_cache = _populate_cache()
# logger.info(f'Seat cache vaules: {OrderedDict(sorted(seats_cache.items()))}')

def get_bookings(current_user: TokenData, db: Database=Depends(get_database)) -> list[model.BookingResponse]:
    bookings_list = [booking for booking in db['bookings'].find({'uid': current_user.get_userid()})] 
    logger.info(f'Retrieved {len(bookings_list)} bookings for user {current_user.get_userid()}')
    return bookings_list

def get_booking_by_id(current_user: TokenData, booking_id: str, db: Database=Depends(get_database)) -> model.Booking:
    if booking := db['booking'].find_one({'_id': ObjectId(booking_id)}) is None:
        logger.warning(status_code=404, detail='Concert not found.')
        raise BookingNotFoundError(booking_id)
    logger.info(f'Retrieved booking {booking_id} for user {current_user.get_userid()}')
    return booking

# def book_tickets(user_id: str=Body(...), concert_id: str=Body(...), seats: List[str]=Body(...)) -> Booking:
#     """
#     Updates booking database based on a (group of) seat(s) a user wishes to pay
#     for. If at least one seat is unavailable in a collection of seats, an error
#     will be thrown. Seats are unavailable if:
#         - GA: there is no more capacity
#         - Other seat types: the specified seat in format SECTION ROW SEAT is 
#             unavailable 

#     :param str user: a user's data
#     :param str conert: concert data
#     :param list[str] seats: a list of seats a user wants to book
#     :return: booking object
#     :raises: 404 error if concert or user not found
#     :raises: 400 error if seat unavailable
#     """

#     # check if concert and user exist
#     if concert := CONCERT_DB.find_one({'concert_id': concert_id}) is None:
#         raise HTTPException(status_code=404, detail='Concert not found.')
    
#     if user := USER_DB.find_one({'_id': ObjectId(user_id)}) is None:
#         raise HTTPException(status_code=404, detail='User not found.')

#     total_price = 0

#     for seat_id in seats:
#         seat = SEAT_DB.find_one({'_id': ObjectId(seat_id)})

#         # check if GA has seats available 
#         if seat['seat_number'] == 'GA' and seats_cache.get(concert_id, 0) == 0:
#             raise HTTPException(status_code=400, detail='No GA seats available.')

#         # check seat availability 
#         if seat is None:
#             raise HTTPException(status_code=400, detail=f'Seat {seat_id} unavailable.')
#         elif seat['status'] == SeatStatus.BOOKED.value:
#             raise HTTPException(status_code=400, detail=f'Seat {seat_id} unavailable.')
#         else:
#             # find seat and add total price
#             seat = SEAT_DB.find_one_and_update({"_id": ObjectId(seat_id)}, {"$set": {"status": SeatStatus.BOOKED.value}})
#             total_price += seat['price']
            
#             # update cache if seat is general admission
#             if seat['seat_number'] == 'GA':
#                 seats_cache[concert_id] -= 1

#     # create booking if successful and return bookign id
#     booking = Booking(
#         user_id=user_id,
#         concert_id=concert_id,
#         seats=seats,
#         total_price=total_price,
#         status=BookingStatus.CONFIRMED.value
#     )

#     new_booking = BOOKING_DB.insert_one(booking.model_dump())
#     created_booking = BOOKING_DB.find_one({'_id': new_booking.inserted_id})
#     return Booking(**created_booking)
    
# @app.patch('/booking/{booking_id}')
# async def cancel_booking(booking_id: str) -> str:
#     """
#     Cancels a booking for a given booking_id. Does not delete the booking in the 
#     database, instead releases the seats booked and changes booking status to 
#     canceled.

#     :param str booking_id: a booking id
#     :return: message confirming cancelation
#     :raises: 400 error if booking already canceled
#     :raises: 404 error if booking_id not found
#     """
#     # find and update booking status to canceled
#     booking = BOOKING_DB.find_one_and_update({"_id": ObjectId(booking_id)}, {"$set": {"status": BookingStatus.CANCELLED.value}})

#     if booking is not None:
#         # check if booking already canceled
#         if booking['status'] == BookingStatus.CANCELLED.value:
#             raise HTTPException(status_code=400, detail=f"Booking already canceled")

#         # get all seats in a booking and update status to available
#         for seat in booking['seats']:
#             SEAT_DB.find_one_and_update({"_id": ObjectId(seat)}, {"$set": {"status": SeatStatus.AVAILABLE.value}})

#         return f'Booking id {booking_id} successfully canceled and associated seats release.'

#     raise HTTPException(status_code=404, detail=f"Booking id {booking_id} not found")
