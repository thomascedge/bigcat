from bson.codec_options import TypeCodec, TypeRegistry
from model import SeatType, SeatStatus, BookingStatus

class EnumCodec(TypeCodec):
    def __init__(self, enum_class):
        self.enum_class = enum_class

    @property
    def python_type(self):
        return self.enum_class
    
    @property
    def bson_type(self):
        return str
    
    def transform_python(self, value):
        return value.value
    
    def transform_bson(self, value):
        return self.enum_class(value)
        
# register codec
TYPE_REGISTRY = TypeRegistry([EnumCodec(SeatType), EnumCodec(SeatStatus), EnumCodec(BookingStatus)])
