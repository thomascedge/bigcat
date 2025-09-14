from pydantic import BaseModel, ConfigDict, BeforeValidator, Field
from enum import Enum
from datetime import datetime
from typing import Optional, Annotated

PyObjectId = Annotated[str, BeforeValidator(str)]

class ConcertStatus(Enum):
    TENTATIVE = 0
    CONFIRMED = 1
    ON_SALE = 2
    SOLD_OUT = 3
    POSTPONED = 4
    CANCELED = 5
    COMPLETED = 6

class Concert(BaseModel):
    id: Optional[PyObjectId] = Field(alias='_id', default=None) # primary key
    uid: str
    artist: str
    tour_name: Optional[str] 
    venue: str
    location: str
    concert_datetime: datetime
    status: Optional[ConcertStatus | int]
    update_datetime: datetime

    model_config = ConfigDict(use_enum_values=True)

class ConcertResponse(BaseModel):
    concert_list: list = list[Concert]

    model_config = ConfigDict(use_enum_values=True)
