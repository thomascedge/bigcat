from pydantic import BaseModel, ConfigDict, BeforeValidator, Field
from enum import Enum
from typing import Optional, Annotated

PyObjectId = Annotated[str, BeforeValidator(str)]

class SeatType(Enum):
    REGULAR = 0
    PREMIUM = 1
    VIP = 2

class SeatStatus(Enum):
    AVAILABLE = 0
    BOOKED = 1
    RESERVED = 2


class Seat(BaseModel):
    id: Optional[PyObjectId] = Field(alias='_id', default=None) # primary key
    uid: str
    concert_id: str
    venue: str
    seat_number: str
    seat_type: SeatType
    price: float
    status: SeatStatus

    model_config = ConfigDict(use_enum_values=True)

class SeatRequest(BaseModel):
    seat_list: list[Seat]

    model_config = ConfigDict(use_enum_values=True)

class SeatResponse(SeatRequest):
    model_config = ConfigDict(use_enum_values=True)
    