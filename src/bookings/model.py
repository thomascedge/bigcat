from pydantic import BaseModel, Field, BeforeValidator, ConfigDict
from enum import Enum
from datetime import datetime
from typing import Optional, Annotated
from uuid import UUID

PyObjectId = Annotated[str, BeforeValidator(str)]

class BookingStatus(Enum):
    PENDING = 0
    CONFIRMED = 1
    CANCELLED = 2

class PaymentStatus(Enum):
    PENDING = 0
    SUCCESS = 1
    FAILED = 2
    CANCELLED = 3
    REFUNDED = 4
    AUTHORIZED = 5


class Booking(BaseModel):
    uid: str
    user_id: str  # foreign key
    concert_id: str # foreign key
    seats: list[str] # foreign keys when exploded
    total_price: float
    payment_status: PaymentStatus
    status: BookingStatus

    model_config = ConfigDict(use_enum_values=True)

class BookingCreate(Booking):
    pass

class BookingRequest(Booking):
    request_datetime: datetime

    model_config = ConfigDict(from_attributes=True, use_enum_values=True)

class BookingResponse(BookingRequest):
    confirmation_id: str
    
    model_config = ConfigDict(from_attributes=True, use_enum_values=True)
