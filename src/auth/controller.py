from fastapi import APIRouter, Depends, Request, status
from fastapi.security import OAuth2PasswordRequestForm
from pymongo.database import Database
from typing import Annotated
from auth import service
from auth.model import *
from database.core import get_database
from rate_limiting import limiter

router = APIRouter(
    prefix='/auth',
    tags=['Auth']
)

@router.post('/', status_code=status.HTTP_201_CREATED)
@limiter.limit('5/hour')
async def register_user(request: Request, register_user_request: RegisterUserRequest, db: Database = Depends(get_database)):
    service.register_user(register_user_request, db)

@router.post('/token', response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Database = Depends(get_database)):
    return service.login_for_access_token(form_data, db)

# @router.patch('/admin/{user_id}')
# async def login_for_access_token(user_id: str, has_rights: bool, db: Database = Depends(get_database)):
#     return service.login_for_access_token(user_id, has_rights, db)
