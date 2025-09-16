from pydantic import BaseModel, EmailStr
from bson.objectid import ObjectId

class RegisterUserRequest(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    password: str
    admin: bool

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    uid: str | None = None

    def get_userid(self) -> str | None:
        if self.uid:
            return str(self.uid)
        return None
    