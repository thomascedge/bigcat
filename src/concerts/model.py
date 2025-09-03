from pydantic import BaseModel, ConfigDict
from enum import Enum
from datetime import datetime

class Concert(BaseModel):
    concert_id: str
    artist: str
    tour_name: str
    venue: str
    location: str
    datetime: datetime

class UserResponse(Concert):
    model_config = ConfigDict(from_attributes=True, use_enum_values=True)

