from fastapi import HTTPException

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
