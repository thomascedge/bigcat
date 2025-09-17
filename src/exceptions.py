from fastapi import HTTPException
from enum import Enum

''' --------------- ADMIN --------------- '''
class NoAdminPermissions(HTTPException):
    def __init__(self):
        super().__init__(status_code=401, detail='User does not have admin permissions.')

''' --------------- BOOKINGS --------------- '''
class BookingUpdateCode(Enum):
    CANCELED = 0
    SEAT_ADDED = 1
    SEAT_REMOVED = 2

class BookingError(HTTPException):
    """Base exception for todo-related errors"""
    pass

class BookingNotFoundError(BookingError):
    def __init__(self, booking_id=None):
        message = "Booking not found" if booking_id is None else f"Booking with id {booking_id} not found"
        super().__init__(status_code=404, detail=message)

class BookingCreationError(BookingError):
    def __init__(self, error: str):
        super().__init__(status_code=500, detail=f"Failed to create booking: {error}")

class BookingAlreadyUpdatedError(BookingError):
    def __init__(self, booking_id: str, code: BookingUpdateCode, seat_id: str=None):
        match code:
            case BookingUpdateCode.CANCELED:
                message = f"Booking with id {booking_id} already canceled."
            case BookingUpdateCode.SEAT_ADDED:
                message = f'Seat {seat_id} already added to booking with id {booking_id}'
            case BookingUpdateCode.SEAT_REMOVED:
                message = f'Seat {seat_id} already removed to booking with id {booking_id}'
        super().__init__(status_code=400, detail=message)


''' --------------- SEATS --------------- '''
class SeatError(HTTPException):
    """Base exception for concert-related errors"""
    pass

class SeatNotFoundError(SeatError):
    def __init__(self, uid=None):
        message = 'Seat not found' if uid is None else f'Seat with id {uid} not found'
        super().__init__(status_code=404, detail=message)

class SeatCreationError(SeatError):
    def __init__(self, error: str):
        super().__init__(status_code=500, detail=f'Failed to create seat: {error}')

class SeatUnavailableError(SeatError):
    def __init__(self, uid=None):
        message = 'Seat not found' if uid is None else f'Seat {uid} is unavailable'
        super().__init__(status_code=400, detail=message)


''' --------------- CONCERTS --------------- '''
class ConcertError(HTTPException):
    """Base exception for concert-related errors"""
    pass

class ConcertNotFoundError(ConcertError):
    def __init__(self, concert_id=None):
        message = 'Concert not found' if concert_id is None else f'Concert with id {concert_id} not found'
        super().__init__(status_code=404, detail=message)

class ConcertCreationError(ConcertError):
    def __init__(self, error: str):
        super().__init__(status_code=500, detail=f'Failed to create concert: {error}')


''' --------------- USERS --------------- '''
class UserError(HTTPException):
    """Base exception for user-related errors"""
    pass

class UserNotFoundError(UserError):
    def __init__(self, user_id=None):
        message = "User not found" if user_id is None else f"User with id {user_id} not found"
        super().__init__(status_code=404, detail=message)

class PasswordMismatchError(UserError):
    def __init__(self):
        super().__init__(status_code=400, detail="New passwords do not match")

class InvalidPasswordError(UserError):
    def __init__(self):
        super().__init__(status_code=401, detail="Current password is incorrect")

class AuthenticationError(HTTPException):
    def __init__(self, message: str = "Could not validate user"):
        super().__init__(status_code=401, detail=message)
