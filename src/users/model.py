from pydantic import BaseModel, EmailStr, BeforeValidator, Field
from datetime import datetime
from typing import Optional, Annotated

PyObjectId = Annotated[str, BeforeValidator(str)]

class User(BaseModel):
    id: Optional[PyObjectId] = Field(alias='_id', default=None) # primary key
    first_name: str
    last_name: str
    email: str
    password_hash: str

class UserResponse(BaseModel):
    id: Optional[PyObjectId] = Field(alias='_id', default=None) # primary key
    first_name: str
    last_name: str
    email: EmailStr
    
class PasswordChange(BaseModel):
    current_password: str
    new_password: str
    new_password_confirm: str
    