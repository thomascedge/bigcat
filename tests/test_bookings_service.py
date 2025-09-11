import pytest
from datetime import datetime
from uuid import uuid4
from src.bookings import service as bookings_service
from src.bookings.model import *
from src.seats.model import Seat, SeatType, SeatStatus
from src.exceptions import (
    BookingUpdateCode,
    BookingNotFoundError,
    BookingAlreadyUpdatedError,
    BookingCreationError
)
from src.logging import logger

class TestBookingService:
    def test_get_booking_by_id(self, test_user, test_booking, db_session):
        db_session['booking'].insert_one(test_booking.model_dump())

        booking = bookings_service.get_booking_by_id(test_user, test_booking.uid, db_session)
        assert booking.uid == test_booking.uid

    def test_search_booking(self, test_user, test_booking, db_session):
        db_session['booking'].insert_one(test_booking.model_dump())

        query = {
            'booking_id': test_booking.uid,
            'venue': 'TESTVENUE'
        }

        bookings = bookings_service.search_booking(test_user,
                                                  booking_id=query['booking_id'],
                                                  db=db_session)
        assert len(bookings.booking_list) > 0
        assert any(booking.uid == query['booking_id'] for booking in bookings.booking_list)

        bookings = bookings_service.search_booking(test_user,
                                                  venue=query['venue'],
                                                  db=db_session)
        assert len(bookings.booking_list) > 0
        assert any(booking.uid == query['booking_id'] for booking in bookings.booking_list)

        with pytest.raises(BookingNotFoundError):
            bookings_service.get_booking_by_id(test_user, '', db_session)

    def test_book_tickets(self, test_user, test_booking, test_concert, test_seat, db_session):
        db_session['booking'].insert_one(test_booking.model_dump())
        db_session['concert'].insert_one(test_concert.model_dump())
        db_session['seat'].insert_one(test_seat.model_dump())
        booking = bookings_service.book_tickets(test_user, 'TESTCONCERT',[test_seat.uid], db_session)
        assert booking.concert_id == booking.concert_id

        with pytest.raises(BookingCreationError):
            bookings_service.book_tickets(test_user, '', None, db_session)

    def test_add_seat_to_booking(self, test_user, test_booking, test_seat_2, db_session):
        db_session['booking'].insert_one(test_booking.model_dump())
        db_session['seat'].insert_one(test_seat_2.model_dump())

        updated_booking = bookings_service.add_seat_to_booking(test_user, test_booking.uid, test_seat_2.uid, db_session)
        assert test_seat_2.uid in updated_booking.seats

        with pytest.raises(BookingNotFoundError):
            bookings_service.add_seat_to_booking(test_user, '', None, db_session)
        
        with pytest.raises(BookingAlreadyUpdatedError):
            bookings_service.add_seat_to_booking(test_user, test_booking.uid, test_seat_2.uid, db_session)

    def test_remove_seat_from_booking(self, test_user, test_booking, test_seat_2, db_session):
        db_session['booking'].insert_one(test_booking.model_dump())
        db_session['seat'].insert_one(test_seat_2.model_dump())
        
        _ = bookings_service.add_seat_to_booking(test_user, test_booking.uid, test_seat_2.uid, db_session)
        updated_booking = bookings_service.remove_seat_from_booking(test_user, test_booking.uid, test_seat_2.uid, db_session)
        assert test_seat_2.uid not in updated_booking.seats

        with pytest.raises(BookingNotFoundError):
            bookings_service.remove_seat_from_booking(test_user, '', None, db_session)
        
        with pytest.raises(BookingAlreadyUpdatedError):
            bookings_service.remove_seat_from_booking(test_user, test_booking.uid, test_seat_2.uid, db_session)

    def test_cancel_booking(self, test_user, test_booking, test_seat_2, db_session):
        db_session['booking'].insert_one(test_booking.model_dump())

        updated_booking = bookings_service.cancel_booking(test_user, test_booking.uid, db_session)
        assert updated_booking.status == BookingStatus.CANCELED.value

        with pytest.raises(BookingNotFoundError):
            bookings_service.cancel_booking(test_user, '', db_session)

        with pytest.raises(BookingAlreadyUpdatedError):
            bookings_service.cancel_booking(test_user, test_booking.uid, db_session)

    def test_edit_booking(self, test_user, test_booking, test_booking_2, db_session):
        db_session['booking'].insert_one(test_booking.model_dump())

        updated_booking = bookings_service.edit_booking(test_user, test_booking.uid, test_booking_2, db_session)
        assert updated_booking.payment_status == test_booking_2.payment_status
        assert updated_booking.status == test_booking_2.status
        