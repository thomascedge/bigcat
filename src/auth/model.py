from pydantic import BaseModel, EmailStr
from bson.objectid import ObjectId

class RegisterUserRequest(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    user_id: str | None = None

    def get_userid(self) -> str | None:
        if self.user_id:
            return str(self.user_id)
        return None