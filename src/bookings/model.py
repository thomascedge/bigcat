from pydantic import BaseModel, Field, BeforeValidator, ConfigDict
from enum import Enum
from datetime import datetime
from typing import Optional, Annotated

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


class BookingBase(BaseModel):
    id: Optional[PyObjectId] = Field(alias='_id', default=None) # primary key
    user_id: str  # foreign key
    concert_id: str # foreign key
    seats: list[str] # foreign keys when exploded
    total_price: float
    payment_status: PaymentStatus

class BookingCreate(BookingBase):
    pass

class BookingRequest(BookingBase):
    request_datetime: datetime

    model_config = ConfigDict(from_attributes=True)

class BookingResponse(BookingRequest):
    confirmation_id: str
    status: int
    
    model_config = ConfigDict(from_attributes=True)
