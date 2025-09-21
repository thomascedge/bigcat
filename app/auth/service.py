import os
import jwt
import bcrypt
from jwt import PyJWTError
from uuid import uuid4
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from pymongo.database import Database
from dotenv import load_dotenv
from typing import Annotated
from datetime import timedelta, datetime, timezone
from passlib.context import CryptContext
from app.loguru_log import logger
from app.exceptions import AuthenticationError
from app.auth.model import *
from app.users.model import User
from app.database.core import get_database

load_dotenv()

db_password = os.getenv('MONGO_PASSWORD')
uri = os.getenv('DATABASE_URI').replace('db_password', db_password)
SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_berer = OAuth2PasswordBearer(tokenUrl='auth/token')
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

def verify_password(plain_password: str, hashed_password: bytes) -> bool:
    return bcrypt_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return bcrypt_context.hash(password)

def authenticate_user(email: str, password: str, db: Database=Depends(get_database)) -> User | bool:
    user = None
    users = db['user'].find({'email': email})

    for user in users:
        if verify_password(password, user['password_hash']):
            break

    if not user or not verify_password(password, user['password_hash']):
        logger.warning(f'Failed authentication attempt for email: {email}')
        return False
    return User(**user)

def create_access_token(email: str, uid: str, admin: bool, expires_delta: timedelta) -> str:
    encode = {
        'sub': email,
        'id': uid,
        'admin': admin,
        'exp': datetime.now(timezone.utc) + expires_delta
    }
    return jwt.encode(encode, SECRET_KEY, ALGORITHM)

def verify_token(token: str) -> TokenData:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])        
        uid: str = payload.get('id')
        admin: bool = payload.get('admin')
        return TokenData(uid=uid, admin=admin)
    except PyJWTError as e:
        logger.warning(f'Token verification failed: {str(e)}')
        raise AuthenticationError()
    

def register_user(register_user_request: RegisterUserRequest, db: Database=Depends(get_database)) -> None:
    try:
        create_user_mode = User(
            uid=str(uuid4()),
            email=register_user_request.email,
            first_name=register_user_request.first_name,
            last_name=register_user_request.last_name,
            password_hash=get_password_hash(register_user_request.password),
            admin=register_user_request.admin
        )
        db['user'].insert_one(create_user_mode.model_dump())
        logger.info(f'Created new user {register_user_request.email}.')
        # return RegisterUserResponse(username=register_user_request.email)
    
    except Exception as e:
        logger.error(f'Failed to register user: {register_user_request.email}. Error {str(e)}')
        raise

def get_current_user(token: Annotated[str, Depends(oauth2_berer)]) -> TokenData:
    return verify_token(token)

CurrentUser = Annotated[TokenData, Depends(get_current_user)]

def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Database=Depends(get_database)) -> Token:
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise AuthenticationError()
    token = create_access_token(user.email, user.uid, user.admin, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    return Token(access_token=token, token_type='bearer')
