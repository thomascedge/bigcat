import pytest
from datetime import datetime
from src.seats import service as seats_service
from src.seats.model import *
from src.exceptions import SeatCreationError, SeatNotFoundError, SeatUnavailableError
from src.logging import logger

class TestSeatsService:
    def test_get_seat_by_id(self, test_seat, db_session):
        db_session['seat'].insert_one(test_seat.model_dump())

        seat = seats_service.get_seat_by_id(test_seat.uid, db_session)
        assert seat.uid == test_seat.uid

        with pytest.raises(SeatNotFoundError):
            seats_service.get_seat_by_id('', db_session)

    def test_search_seats(self, test_concert, test_seat, db_session):
        db_session['seat'].insert_one(test_seat.model_dump())

        seats = seats_service.search_seats(concert_id=test_concert.concert_id, 
                                              db=db_session)
        assert len(seats.seat_list) > 0

        seats = seats_service.search_seats(venue=test_concert.venue, 
                                              db=db_session)
        assert len(seats.seat_list) > 0

    def test_create_seats(self, test_user, test_seat, test_seat_2, db_session):
        db_session['seat'].insert_one(test_seat.model_dump())
        created_seats = seats_service.create_seats(test_user, [test_seat, test_seat_2], db_session)
        assert any(seat.uid == test_seat.uid for seat in created_seats.seat_list)
        assert any(seat.uid == test_seat_2.uid for seat in created_seats.seat_list)

        with pytest.raises(SeatCreationError):
            seats_service.create_seats(test_user, None, db_session)

    def test_edit_seat(self, test_user, test_seat, test_seat_2, db_session):
        db_session['seat'].insert_one(test_seat.model_dump())

        updated_seat = seats_service.edit_seat(test_user, test_seat.uid, test_seat_2, db_session)
        assert updated_seat.seat_number == test_seat_2.seat_number

    def test_delete_seat(self, test_user, test_seat, db_session):
        db_session['seat'].insert_one(test_seat.model_dump())

        seats_service.delete_seat(test_user, test_seat.uid, db_session)
        assert db_session['seat'].find_one({'uid': test_seat.uid}) is None
