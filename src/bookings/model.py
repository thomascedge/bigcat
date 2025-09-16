from pydantic import BaseModel, BeforeValidator, ConfigDict
from enum import Enum
from datetime import datetime
from typing import Optional, Annotated

PyObjectId = Annotated[str, BeforeValidator(str)]

class BookingStatus(Enum):
    PENDING = 0
    CONFIRMED = 1
    CANCELED = 2

class PaymentStatus(Enum):
    PENDING = 0
    SUCCESS = 1
    FAILED = 2
    CANCELED = 3
    REFUNDED = 4
    AUTHORIZED = 5


class Booking(BaseModel):
    uid: str
    user_id: str  # foreign key
    concert_id: str # foreign key
    venue: str
    seats: list[str] # foreign keys when exploded
    total_price: float
    payment_status: PaymentStatus
    status: BookingStatus
    request_datetime: datetime | str
    update_datetime: datetime | str
    confirmation_id: str

    model_config = ConfigDict(use_enum_values=True)


class BookingRequest(BaseModel):
    concert_id: str
    seat_list: list[str]

class UpdateBookingRequest(BaseModel):
    booking_id: str
    booking_update: Booking

    model_config = ConfigDict(use_enum_values=True)

class BookingResponse(BaseModel): 
    booking_list: list[Booking]
       
    model_config = ConfigDict(use_enum_values=True)
