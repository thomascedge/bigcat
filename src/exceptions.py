from fastapi import HTTPException


''' --------------- SEATS --------------- '''
class SeatError(HTTPException):
    """Base exception for concert-related errors"""
    pass

class SeatNotFoundError(SeatError):
    def __init__(self, uid=None):
        message = 'Seat not found' if uid is None else f'Concert with id {uid} not found'
        super().__init__(status_code=404, detail=message)

class SeatCreationError(SeatError):
    def __init__(self, error: str):
        super().__init__(status_code=500, detail=f'Failed to create seat: {error}')


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


''' --------------- BOOKINGS --------------- '''
class BookingError(HTTPException):
    """Base exception for todo-related errors"""
    pass

class BookingNotFoundError(BookingError):
    def __init__(self, booking_id=None):
        message = "Todo not found" if booking_id is None else f"Booking with id {booking_id} not found"
        super().__init__(status_code=404, detail=message)

class BookingCreationError(BookingError):
    def __init__(self, error: str):
        super().__init__(status_code=500, detail=f"Failed to create booking: {error}")


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
