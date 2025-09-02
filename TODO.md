'''--------------  ENUMERATIONS --------------'''
# class SeatType(Enum):
#     REGULAR = 0
#     PREMIUM = 1
#     VIP = 2

# class SeatStatus(Enum):
#     AVAILABLE = 0
#     BOOKED = 1
#     # RESERVED = 2


# class Seat(BaseModel):
#     id: Optional[PyObjectId] = Field(alias='_id', default=None) # primary key
#     concert_id: str # foreign key
#     seat_number: str
#     seat_type: int
#     price: float
#     status: int

# class Concert(BaseModel):
#     id: Optional[PyObjectId] = Field(alias='_id', default=None) # primary key
#     concert_id: str
#     artist: str
#     tour_name: str
#     venue: str
#     location: str
#     datetime: datetime