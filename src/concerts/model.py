from pydantic import BaseModel, ConfigDict
from enum import Enum
from datetime import datetime

class ConcertStatus(Enum):
    TENTATIVE = 0
    CONFIRMED = 1
    ON_SALE = 2
    SOLD_OUT = 3
    POSTPONED = 4
    CANCELED = 5
    COMPLETED = 6

class Concert(BaseModel):
    concert_id: str
    artist: str
    tour_name: str
    venue: str
    location: str
    datetime: datetime
    status: ConcertStatus

    model_config = ConfigDict(use_enum_values=True)

class ConcertResponse(BaseModel):
    concert_list = list[Concert]

    model_config = ConfigDict(use_enum_values=True)
